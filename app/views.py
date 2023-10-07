
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views import View
from django.http import JsonResponse
from . models import Product, Customer, Cart, Category, Order, CustomUser
from django.db.models import Count
from . forms import CustomerRegistrationForm, CustomerProfileForm, Customer, LoginForm
from django.contrib import messages
from django.db.models import Q

# Create your views here.

def about(request):
    return render(request, "app/about.html")

def contact(request):
    return render(request, "app/contact.html")

def orders(request):
    return render(request, "app/orders.html")


def category_list(request):
    categories = Category.objects.filter(parent_category = None)
    return render(request, 'app/home.html', {'categories': categories})

def category_detail(request, category_id):
    category = Category.objects.get(pk=category_id)
    subcategories = category.subcategories.all()
    products = Product.objects.filter(category=category)
    return render(request, 'app/category.html', {'category': category, 'subcategories': subcategories, 'products': products })

def product_filter(request):
    query = request.GET.get('q')
    products = Product.objects.filter(Q(name__icontains=query) | Q(category__name__icontains=query))
    return render(request, 'app/product_filter.html', {'products': products})

class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_product =Product.objects.filter(item=1)

        return render(request, "app/productdetail.html", locals())


class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Bienvenido!, Usuario registrado con éxito")
            return redirect('login')
        else:
            messages.warning(request, "Datos inválidos")
        return render(request, 'app/customerregistration.html', locals())

class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, "¡Felicidades! Datos guardados satisfactoriamente")
        else:
            messages.warning(request, "Datos inválidos")

        return render(request, 'app/profile.html', locals())

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', locals())

class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm()
        return render(request, 'app/updateAddress.html', locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "¡Felicidades! Perfil actualizado satisfactoriamente")
        else:
            messages.warning(request, "Datos inválidos")
        return redirect('address')

def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')


def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.selling_price
        amount = amount + value
    totalamount = amount
    return render(request, 'app/addtocart.html', locals())


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.selling_price
            amount = amount + value
        totalamount = amount
        data={
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.selling_price
            amount = amount + value
        totalamount = amount
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.selling_price
            amount = amount + value
        totalamount = amount
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)


def search(request):
    query = request.GET['search']
    product = Product.objects.filter(Q(name__icontains=query))
    return render(request, 'app/search.html', locals())


def create_order(request):

    if request.method == 'POST':
        delivery_option = request.POST.get('delivery_option')
        address = request.POST.get('address')
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        selected_products = [item.product for item in cart_items]
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.selling_price
            famount = famount + value
        totalamount = famount

        if delivery_option == 'despacho' and address:
            order = Order.objects.create(
                user = request.user,
                delivery_option=request.POST.get('delivery_option'),
                address = address,
                total_price=totalamount,
            )
        elif delivery_option == 'retiro':
            order = Order.objects.create(
                user = request.user,
                delivery_option=request.POST.get('delivery_option'),
                total_price=totalamount,
            )
        

        order.products.set(selected_products)
        cart_items.delete()

        return redirect('list_orders')
    
    cart_items=Cart.objects.filter(user=request.user)
    return render(request, 'app/checkout.html', {'cart_items':cart_items})


def list_orders(request):
    # Retrieve orders for the current user
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'app/list_orders.html', {'orders': orders})







