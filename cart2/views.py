from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from cart2.forms import CartAddProductForm
from cart2.cart import Cart
from website.models import Menu
from django.http import HttpResponseRedirect


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart_detail.html', {'cart': cart})

def cart_add(requset, product_id):
    cart = Cart(requset)
    product = get_object_or_404(Menu, id=product_id)
    cart.add(product)
    return redirect('/')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Menu, id=product_id)
    cart.remove(product_id)
    print(product.name, product.price, product)
    return redirect('/')


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart2:cart_detail")

# def cart_detail(request):
#     cart = Cart(request)
#     for item in cart:
#         item['update_product_count_form'] = CartAddProductForm(
#             initial={'product_count': item['product_count'],
#                      'update': True})
#     return render(request, 'index.html', {'cart': cart})

    