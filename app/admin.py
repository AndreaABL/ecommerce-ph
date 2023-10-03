from django.contrib import admin
from . models import Product, Customer, Cart, Category, Order
from django.urls import reverse
from django.utils.html import format_html
from .signals import order_status_changed
from django.core.mail import send_mail
# Register your models here.

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'category', 'product_image', 'stock']
    search_fields = ['name']
    actions = ['increase_stock', 'decrease_stock']

    def increase_stock(self, request, queryset):
        for product in queryset:
            product.stock += 1
            product.save()

    def decrease_stock(self, request, queryset):
        for product in queryset:
            if product.stock > 0:
                product.stock -= 1
                product.save()

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_category']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','name','locality','city','state','zipcode']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=['id', 'user', 'product', 'quantity']
    def products(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)



def change_order_status_and_notify_customer(modeladmin, request, queryset):
    for order in queryset:
        new_status = 'Cotización enviada'
        order.status = new_status
        order.save()

        order_status_changed.send(sender=Order, order=order, new_status=new_status)
        subject = f'El estado de la orden ha cambiado: Order ID {order.id}'
        message = f'Su orden (Order ID: {order.id}) ha cambiado de estado a {new_status}, revise aqui: http://proyectoshidraulicos.pythonanywhere.com/orders/'
        from_email = 'practicaproyectoshidraulicos@gmail.com'
        recipient_list = [order.customer.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)
change_order_status_and_notify_customer.short_description = 'Cambio en el estado de la orden'

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'pdf_file']
    actions = [change_order_status_and_notify_customer]

    def pdf_file(self, obj):
        if obj.pdf_file:
            return '<a href="%s" target="_blank">View / Download PDF</a>' % obj.pdf_file.url
        else:
            return 'No PDF'
    pdf_file.short_description = 'PDF File'
    pdf_file.allow_tags = True

admin.site.register(Order, OrderAdmin)



