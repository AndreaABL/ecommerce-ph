from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import User
from . models import Customer, Order, CustomUser

STATE_CHOICES = (
    ('Región de Arica y Parinacota', 'Región de Arica y Parinacota'),
    ('Región de Tarapacá','Región de Tarapacá'),
    ('Región de Antofagasta','Región de Antofagasta'),
    ('Región de Atacama', 'Región de Atacama'),
    ('Región de Coquimbo','Región de Coquimbo'),
    ('Región de Valparaíso','Región de Valparaíso'),
    ('Región Metropolitana','Región Metropolitana'),
    ('Región de Libertador General Bernardo O\'Higgins','Región de Libertador General Bernardo O\'Higgins'),
    ('Región del Maule','Región del Maule'),
    ('Región del Biobio','Región del Biobio'),
    ('Región de la Araucanía','Región de la Araucanía'),
    ('Región de Los Ríos','Región de los Ríos'),
    ('Región de Los Lagos', 'Región de Los Lagos'),
    ('Región de Aysén','Región de Aysén'),
    ('Región de Magallanes','Región de Magallanes'),


)

class CustomerRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(label='Nombre', widget=forms.TextInput(attrs={'autofocus':'True', 'class':'form-control'}))
    last_name = forms.CharField(label='Apellido', widget=forms.TextInput(attrs={'autofocus':'True', 'class':'form-control'}))
    state = forms.ChoiceField(label='Región', choices=STATE_CHOICES, widget=forms.Select(attrs={'autofocus':'True', 'class':'form-control'}))
    locality = forms.CharField(label='Ciudad', widget=forms.TextInput(attrs={'autofocus':'True', 'class':'form-control'}))
    city = forms.CharField(label='Comuna', widget=forms.TextInput(attrs={'autofocus':'True', 'class':'form-control'}))
    mobile = forms.CharField(label='Contacto', widget=forms.NumberInput(attrs={'autofocus':'True', 'class':'form-control'}))
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirme su contraseña', widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['email','first_name','last_name','state','locality','city', 'mobile','password1','password2']


class LoginForm(AuthenticationForm):
    username = UsernameField(label="Email", widget=forms.EmailInput(attrs={'autofocus':'True', 'class':'form-control'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput({'autocomplete':'current-password', 'class':'form-control'}))


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label= 'Contraseña actual', widget=forms.PasswordInput(attrs={'autofocus':'True', 'autocomplete':'current-password', 'class':'form-control'}))
    new_password1 = forms.CharField(label='Contraseña nueva', widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class':'form-control'}))
    new_password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='Nueva contraseña', widget = forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))
    new_password2 = forms.CharField(label='Confirmar nueva contraseña', widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'mobile', 'state', 'zipcode']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'locality':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'mobile':forms.NumberInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
            'zipcode':forms.TextInput(attrs={'class':'form-control'}),
        }

