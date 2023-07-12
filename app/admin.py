from django.contrib import admin
from . models import Product, Customer, Cart, Payment, OrderPlaced, Category
from django.urls import reverse
from django.utils.html import format_html
# Register your models here.

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'category', 'product_image', 'stock']
    search_fields = ['name']
    actions = ['increase_stock', 'decrease_stock']

    def increase_stock(self, request, queryset):
        for product in queryset:
            product.stock_quantity += 1
            product.save()

    def decrease_stock(self, request, queryset):
        for product in queryset:
            if product.stock_quantity > 0:
                product.stock_quantity -= 1
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

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display=['id', 'user', 'amount', 'mercadopago_order_id', 'mercadopago_payment_status', 'mercadopago_payment_id', 'paid']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display=['id', 'customer', 'product', 'quantity', 'ordered_date', 'status', 'payment']


