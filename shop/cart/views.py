# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from zenitsu_shop.models import Product, ProductSize, Size
from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST, product=product)
    if form.is_valid():
        cd = form.cleaned_data
        size = cd['size']
        product_size = ProductSize.objects.filter(product=product, size=size).first()
        if product_size and product_size.quantity >= cd['quantity']:
            cart.add(
                product=product,
                size=size,
                quantity=cd['quantity'],
                update_quantity=cd['update']
            )
        else:
            return render(request, 'cart/detail.html', {
                'cart': cart,
                'error': f"Недостаточно товара {product.name} в размере {size.name}. Доступно: {product_size.quantity if product_size else 0}."
            })
    return redirect('cart:cart_detail')

@require_POST
def cart_update(request, product_id, size_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    size = get_object_or_404(Size, id=size_id)
    quantity = int(request.POST.get('quantity'))
    
    # Проверяем наличие товара в выбранном размере
    product_size = ProductSize.objects.filter(product=product, size=size).first()
    if product_size and product_size.quantity >= quantity:
        cart.add(
            product=product,
            size=size,
            quantity=quantity,
            update_quantity=True  # Обновляем количество
        )
    else:
        return render(request, 'cart/detail.html', {
            'cart': cart,
            'error': f"Недостаточно товара {product.name} в размере {size.name}. Доступно: {product_size.quantity if product_size else 0}."
        })
    return redirect('cart:cart_detail')

def cart_remove(request, product_id, size_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    size = get_object_or_404(Size, id=size_id)
    cart.remove(product, size)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})