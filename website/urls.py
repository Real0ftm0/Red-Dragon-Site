from django.urls import path
from website.views import *
from . import views
from django.contrib.auth import views as auth_views
from allauth.account.views import LoginView, SignupView 


app_name = 'website'


urlpatterns = [
    path('', index_view, name = 'index'), 
    path('menu.html', menu_view, name = 'menu'), 
    path('about', about_view, name = 'about'),
    path('index.html', contact_view, name = 'contact'), 
    
    path('login', login_view, name='login' ),

    # path('to-bank/', views.to_bank, name='to_bank'),
    path('order_details', views.callback, name='order_details'),
    
    path('order_details2', order_details_view, name='order_details2'),
]
