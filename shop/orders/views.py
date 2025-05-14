# orders/views.py
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.template.loader import render_to_string
from cart.cart import Cart
from .forms import OrderCreateForm
from zenitsu_shop.models import Order, OrderItem, PaymentMethod, DeliveryMethod, ProductSize
from yookassa import Configuration, Payment
import uuid
import logging
import datetime

logger = logging.getLogger(__name__)

Configuration.configure(settings.YOOKASSA_SHOP_ID, settings.YOOKASSA_SECRET_KEY)

def order_create(request):
    cart = Cart(request)
    if not cart:
        return redirect('cart:cart_detail')

    if not PaymentMethod.objects.exists():
        return HttpResponse("❌ Способы оплаты не настроены. Обратитесь к администратору.")
    if not DeliveryMethod.objects.exists():
        return HttpResponse("❌ Способы доставки не настроены. Обратитесь к администратору.")

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()

            # Создаём элементы заказа и вычитаем количество
            order_items = []
            for item in cart:
                product_size = ProductSize.objects.filter(
                    product=item['product'],
                    size=item['size']
                ).first()
                if product_size and product_size.quantity >= item['quantity']:
                    order_item = OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        size=item['size'],  # Сохраняем размер
                        price=item['price'],
                        quantity=item['quantity']
                    )
                    # Вычитаем количество из ProductSize
                    product_size.quantity -= item['quantity']
                    product_size.save()
                    order_items.append(order_item)
                else:
                    return HttpResponse(f"❌ Недостаточно товара {item['product'].name} в размере {item['size'].name}.")

            order_total = cart.get_total_price()
            delivery_cost = order.delivery.price
            total_cost = order_total + delivery_cost

            order.total_cost = total_cost
            order.save()

            try:
                idempotence_key = str(uuid.uuid4())
                payment = Payment.create({
                    "amount": {
                        "value": str(total_cost),
                        "currency": "RUB"
                    },
                    "confirmation": {
                        "type": "redirect",
                        "return_url": settings.YOOKASSA_RETURN_URL
                    },
                    "capture": True,
                    "description": f"Заказ #{order.id} (с доставкой: {order.delivery.name})",
                    "metadata": {
                        "order_id": order.id
                    }
                }, idempotence_key)

                order.yookassa_payment_id = payment.id
                order.save()

                try:
                    subject = f'Подтверждение заказа #{order.id}'
                    html_message = render_to_string('orders/email_order_confirmation.html', {
                        'order': order,
                        'items': order_items,
                        'delivery_cost': delivery_cost,
                        'total_cost': total_cost,
                        'return_url': payment.confirmation.confirmation_url,
                        'year': datetime.datetime.now().year,
                    })
                    email = EmailMessage(
                        subject,
                        html_message,
                        settings.EMAIL_HOST_USER,
                        [order.email],
                    )
                    email.content_subtype = 'html'
                    email.send()
                except Exception as e:
                    logger.error(f"Ошибка отправки письма: {str(e)}")

                cart.clear()
                return redirect(payment.confirmation.confirmation_url)

            except Exception as e:
                logger.error(f"Ошибка создания платежа: {str(e)}")
                return HttpResponse(f"❌ Ошибка создания платежа: {str(e)}")

        else:
            return render(request, 'orders/create.html', {'cart': cart, 'form': form})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})