from django.conf import settings
from website.models import Menu
from decimal import Decimal

class Cart(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Menu.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            # item['total_price'] = item['price'] * item['product_count']
            item['price'] = Decimal(item['price'])
            # item['product'] = Menu.objects.get(id=int(item['id']))
            item['total_price'] = int(item['price']) * int(item['product_count'])
            yield item

    def add(self, product, product_count=1, update_count=False): 
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'product_count': 0,
                                     'price': str(product.price)}

        if update_count:
            self.cart[product_id]['product_count'] = int(product_count)
        else:
            self.cart[product_id]['product_count'] += int(product_count)
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __len__(self):
        return sum(item['product_count'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['product_count'] for item in self.cart.values())

    def clear(self):
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True
