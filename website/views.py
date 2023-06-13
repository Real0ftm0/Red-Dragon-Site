from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.http import HttpResponse
from . import models
from website.models import Menu
from website.forms import ContactForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required
#from cart2.forms import CartAddProductForm
from cart2.cart import Cart
from decimal import Decimal
from zeep import Client
from django.contrib.auth.models import User
from django.core.mail import send_mail


def index_view(request):
    menu = Menu.objects.filter(type = "food").order_by('-price')
    menu_drink = Menu.objects.filter(type = "drink").order_by('-price')
    
    context = {'menu': menu, 'menu_drink': menu_drink}

    return render(request, 'index.html', context)

def login_view(request):
    return render(request, 'account/login.html')

@login_required
def order_details_view(request):
    cart = Cart(request)
    is_order = False
    if request.method == 'POST':
        order = models.Order.objects.create(customer=request.user)
        for item in cart:
            models.OrderItem.objects.create(order=order,
                                            product=item['product'],
                                            product_price=item['price'],
                                            product_count=item['product_count'],
                                            product_cost=Decimal(item['product_count']) * Decimal(item['price']))
        cart.clear()
    order_count = models.OrderItem.objects.filter(order__customer=request.user)
    order_price = sum(item.product_price * item.product_count for item in order_count)
    if models.Order.objects.all():
        is_order = True

    return render(request, 'order_details.html', {'cart': cart, 'is_order': is_order, 'order_count': order_count.count(), 'order_price': order_price})

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        family_name = request.POST.get('family_name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
    
    return render(request, 'index.html')

def about_view(request):
    return render(request, 'about.html')

def menu_view(request):
    menu = Menu.objects.filter(type = "food").order_by('-price')
    menu_drink = Menu.objects.filter(type = "drink").order_by('-price')
    context = {'menu': menu, 'menu_drink': menu_drink}
    
    return render(request, 'menu.html', context)

@login_required
def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        order = models.Order.objects.create(customer=request.user)
        for item in cart:
            models.OrderItem.objects.create(order=order,
                                            product=item['product'],
                                            product_price=item['price'],
                                            product_count=item['product_count'],
                                            product_cost=Decimal(item['product_count']) * Decimal(item['price']))
            
        # order.customer = request.user
        # order.save()
        cart.clear()
        return render(request, 'order_detail.html', {'order': order})
    return render(request, 'test.html', {'cart': cart})


def product(request, pk):
    product_detail = get_object_or_404(models.Menu, id=pk)
    return render(request, 'product.html', {'product_detail': product_detail})


merchant = '********-****-****-****-************'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')

@login_required
def to_bank(request):
    #checkout 
    cart = Cart(request)
    if request.method == 'POST':
        order = models.Order.objects.create(customer=request.user)
        for item in cart:
            models.OrderItem.objects.create(order=order,
                                            product=item['product'],
                                            product_price=item['price'],
                                            product_count=item['product_count'],
                                            product_cost=Decimal(item['product_count']) * Decimal(item['price']))
            
        # order.customer = request.user
        # order.save()
        cart.clear()

    #to_bank     
    amount = 0
    order_items = models.OrderItem.objects.filter(order=order)
    for item in order_items:
        amount += item.product_cost
    callbackUrl = 'http://127.0.0.1:8000/callback/'
    mobile = ''
    email = ''
    description = 'Test'
    result = client.service.PaymentRequest(merchant, amount, description, email, mobile, callbackUrl)

    if result.Status == 100 and len(result.Authority) == 36:
        models.Invoice.objects.create(order=order,
                                      authority=result.Authority)
        return redirect('https://www.zarinpal.com/pg/StartPay/' + result.Authority)
    else:
        return HttpResponse('Error code ' + str(result.Status))


def callback(request):
    if request.GET.get('Status') == 'OK':
        authority = request.GET.get('Authority')
        invoice = get_object_or_404(models.Invoice, authority=authority)
        amount = 0
        order = invoice.order
        order_items = models.OrderItem.objects.filter(order=order)
        for item in order_items:
            amount += item.product_cost
        result = client.service.PaymentVerification(merchant, authority, amount)
        if result.Status == 100:
            return render(request, 'order_details', {'invoice': invoice})
        else:
            return HttpResponse('error ' + str(result.Status))
    else:
        return HttpResponse('error ')
