# cart/cart.py
from decimal import Decimal
from django.conf import settings
from zenitsu_shop.models import Product, Size

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, size, quantity=1, update_quantity=False):
        key = f"{product.id}_{size.id}"
        if key not in self.cart:
            self.cart[key] = {
                'product_id': product.id,
                'size_id': size.id,
                'quantity': 0,
                'price': str(product.price)
            }
        if update_quantity:
            self.cart[key]['quantity'] = quantity
        else:
            self.cart[key]['quantity'] += quantity
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product, size):
        key = f"{product.id}_{size.id}"
        if key in self.cart:
            del self.cart[key]
            self.save()

    def __iter__(self):
        product_ids = [int(key.split('_')[0]) for key in self.cart.keys()]
        products = Product.objects.filter(id__in=product_ids)
        product_dict = {product.id: product for product in products}

        size_ids = [int(key.split('_')[1]) for key in self.cart.keys()]
        sizes = Size.objects.filter(id__in=size_ids)
        size_dict = {size.id: size for size in sizes}

        for key, item in self.cart.items():
            product = product_dict.get(item['product_id'])
            size = size_dict.get(item['size_id'])
            if product and size:
                item['product'] = product
                item['size'] = size
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['quantity']
                yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True