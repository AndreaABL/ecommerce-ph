from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from . forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm
from .views import *
from django.urls import path, include

urlpatterns = [
    path('' , views.category_list, name='home'),
    path('about/', views.about, name = "about"),
    path('contact/', views.contact,name="contact"),
    path('irrigat/', views.irrigat,name="irrigat"),
    path('products/without-category/', views.products_without_category, name='products_without_category'),
    path('categories/<int:category_id>/', views.category_detail, name='category_detail'),



    path('product-detail/<int:pk>', views.ProductDetail.as_view(), name="product-detail"),
    path('profile/', views.user_profile, name='profile'),
    path('profile/update', views.update_profile, name='address'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('checkout/', views.create_order, name='create_order'),
    path('orders/', views.list_orders, name='list_orders'),


    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('search/', views.search, name='search'),

    #login
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm), name='login'),

    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone'), name='passwordchange'),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name="passwordchangedone"),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),

    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class = MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
