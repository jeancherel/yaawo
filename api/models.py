from django.db import models
from django.core import validators

class Store(models.Model):
    name = models.CharField(max_length=25)
    phone = models.CharField(max_length=10, unique=True, validators=[
        validators.RegexValidator("(01|05|07)[0-9]{8}$", message="Numéro de téléphone invalide"),
    ])
    adress = models.CharField(max_length=300, validators=[
        validators.MinLengthValidator(30, message="L'adresse doit contenir au moins 30 caractères")
    ], blank=True)
    # description = models.CharField(max_length=300)
    official_page = models.URLField(verbose_name="Page officielle", null=True)
    is_online_only = models.BooleanField(default=False)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey('authentication.User', related_name='stores', on_delete=models.CASCADE)

class Product(models.Model):
    name = models.CharField(max_length=25)
    price = models.IntegerField()
    description = models.CharField(max_length=300)
    image = models.ImageField(upload_to="products/")
    quantity = models.IntegerField()
    store = models.ForeignKey(Store, related_name="products", on_delete=models.CASCADE)

class Receipt(models.Model):
    date = models.DateTimeField(auto_now=True)
    total_price = models.IntegerField()
    customer = models.ForeignKey('authentication.User', on_delete=models.DO_NOTHING)
    payment_method = models.CharField(max_length=25)
    state = models.IntegerField(default=0)

class Order(models.Model):
    date = models.DateTimeField(auto_now=True)
    ordered_quantity = models.IntegerField()
    total_price = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)