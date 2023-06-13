from django.contrib import admin
# from website.models import Menu, Order
# from website.models import Contact 
from . import models

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    list_display = ('name', 'name_farsi' , 'type' , 'price', 'created_date') 
    list_filter = ('name',)
    search_fields = ('name', 'price', )


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order_date',)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice', 'amount', 'transaction_date', 'status')


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'order',)

class ContactAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    list_display = ('name', 'email', 'created_date') 
    list_filter = ('email',)
    search_fields = ('name', 'email', 'message')


admin.site.register(models.Menu, ProductAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem, OrderItemAdmin)
admin.site.register(models.Invoice, InvoiceAdmin)
admin.site.register(models.Transaction, TransactionAdmin)
admin.site.register(models.Contact, ContactAdmin)

    