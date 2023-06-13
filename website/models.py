from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse


class Menu(models.Model):
    name = models.CharField(max_length=255)
    name_farsi = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    image = models.ImageField( upload_to= 'img/', default= 'food/default.jpg')
    price = models.FloatField()
    description = models.TextField(blank = True , null=True)
    created_date = models.DateTimeField(auto_now_add= True)
    update_date = models.DateTimeField(auto_now= True)

    class Meta: 
        ordering = ('created_date',) 
        
    def __str__(self):
        return self.name 
    
    def get_absolute_url(self):
        return reverse('shop:product', args=[self.id])


class Order(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Menu, null=True, on_delete=models.SET_NULL)
    product_price = models.DecimalField(max_digits=10, decimal_places=0)
    product_count = models.PositiveIntegerField()
    product_cost = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return str(self.id)


class Invoice(models.Model):
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    invoice_date = models.DateTimeField(auto_now_add=True)
    authority = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.id)


class Transaction(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('failed', 'Failed'),
        ('completed', 'Completed')
    )
    invoice = models.ForeignKey(Invoice, null=True, on_delete=models.SET_NULL)
    transaction_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return str(self.id)

    
class Contact(models.Model):
    name = models.CharField(max_length=255)
    family_name = models.CharField(max_length=255, blank = True , null=True)
    email = models.EmailField()
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add= True)
    update_date = models.DateTimeField(auto_now= True)

    class Meta: 
        ordering = ('created_date',) 
        
    def __str__(self):
        return self.name 
        
