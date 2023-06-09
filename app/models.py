
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
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


CATEGORY_CHOICES = (
    ('BO', 'Bombas'),
    ('EL', 'Electricidad'),
    ('PP', 'Polietileno'),
    ('RE', 'Revestimiento'),
    ('TU', 'Tuberia'),
)

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcategories')
    category_image = models.ImageField(upload_to='category')
    subcategory_image = models.ImageField(upload_to='subcategory')

    def __str__(self):
        return self.name
class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    selling_price = models.IntegerField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    product_image = models.ImageField(upload_to='product')
    stock = models.IntegerField(default=0)
    item = models.BooleanField(default=False, help_text='0=default, 1=item')

    def __str__(self) :
        return self.name

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Nombre',max_length=200)
    locality = models.CharField(verbose_name='Comuna', max_length=200)
    city = models.CharField(verbose_name='Ciudad' ,max_length=50)
    mobile = models.IntegerField(verbose_name='Teléfono' ,default=0)
    zipcode = models.IntegerField(verbose_name='Código postal')
    state = models.CharField(verbose_name='Región', choices=STATE_CHOICES, max_length=100)

    def __str__(self) :
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price


STATUS_CHOICES = (
    ('Aceptado', 'Aceptado'),
    ('Empacado', 'Empacado'),
    ('En camino', 'En camino'),
    ('Enviado', 'Enviado'),
    ('Cancelado', 'Cancelado'),
    ('Pendiente', 'Pendiente'),
)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    mercadopago_order_id = models.CharField(max_length=100, blank=True, null=True)
    mercadopago_payment_status = models.CharField(max_length=100, blank=True, null=True)
    mercadopago_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)

    @property
    def __str__(self):
        return self.description

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pendiente')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default="")

    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price

