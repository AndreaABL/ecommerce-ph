
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import JsonResponse
from . models import Product,  Cart, Category, Order, OrderItem
from . forms import CustomerRegistrationForm, CustomerProfileForm, ProductSearchForm, InformationForm
from django.db.models import Q
from django.contrib import messages

# Create your views here.

def about(request):
    return render(request, "app/about.html")

def contact(request):
    if request.method == 'POST':
        form = InformationForm(request.POST)
        if form.is_valid():
            # Process the form data and send an email
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            description = form.cleaned_data['description']

            # Send an email to the administrator
            subject = 'Nuevo mensaje'
            message = f'Nombre: {name}\nEmail: {email}\nDescripción: {description}'
            from_email = email
            recipient_list = ['administracion@proyectoshidraulicos.cl']
            send_mail(subject, message, from_email, recipient_list)
            

            # You can also save the form data to a database here
    else:
        form = InformationForm()
    return render(request, "app/contact.html", {'form':form})

def irrigat(request):
    return render(request, "app/irrigat.html")

def orders(request):
    return render(request, "app/orders.html")

def products_without_category(request):
    productss = Product.objects.filter(category=None)
    return render(request, 'app/products_without_category.html', {'productss': productss})

def category_list(request):
    categories = Category.objects.filter(parent_category = None)
    return render(request, 'app/home.html', {'categories': categories})

def menu_view(request):
    categories = Category.objects.filter(parent_category__isnull=True)  # Get top-level categories
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

@login_required
def user_profile(request):
    custom_user = request.user
    context = {
        'custom_user' : custom_user,
    }

    return render(request, 'app/profile.html', context)

@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect(user_profile)
    else:
        form = CustomerProfileForm()
    context = {
        'form':form,
    }
    return render(request, 'app/address.html', context)

@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')


@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.selling_price
        amount = amount + value
    totalamount = amount
    return render(request, 'app/addtocart.html', locals())

@login_required
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

@login_required
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

@login_required
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
    if request.method == 'GET':
        form = ProductSearchForm(request.GET)
        if form.is_valid():
            search_term = form.cleaned_data.get('search')
            products = Product.objects.filter(name__icontains=search_term)
        else:
            products = Product.objects.all()
    else: 
        form = ProductSearchForm()
        products = Product.objects.all()
    context = {
        'products' : products,
        'form' : form,
    }

    return render(request, 'app/search.html', context)


@login_required
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
        for cart_item in cart_items:
            OrderItem.objects.create(
                order = order, 
                product = cart_item.product, 
                quantity = cart_item.quantity,
                user = request.user,
            )
        order.products.set(selected_products)
        cart_items.delete()

        return redirect('list_orders')
    
    cart_items=Cart.objects.filter(user=request.user)
    return render(request, 'app/checkout.html', {'cart_items':cart_items})

@login_required
def list_orders(request):
    # Retrieve orders for the current user
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'app/list_orders.html', {'orders': orders})




