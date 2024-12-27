from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators

class User(AbstractUser):

    class AccountTypes(models.TextChoices):
        SELLER = "SELLER", "Vendeur"
        BUYER = "CUSTOMER", "Client"

    phone = models.CharField(max_length=10, unique=True, validators=[
        validators.RegexValidator("(01|05|07)[0-9]{8}$", message="Numéro de téléphone invalide"),
    ], verbose_name="Numéro de téléphone")
    adress = models.CharField(max_length=255, validators=[
        validators.MinLengthValidator(10, message="L'adresse doit contenir au moins 10 caractères")
    ], verbose_name="Adresse")
    id_picture = models.ImageField(verbose_name="Photo d'identité", upload_to="id_picture/")
    id_piece = models.ImageField(verbose_name="Pièce d'identité", upload_to="id_piece/", null=True)
    account_type = models.CharField(verbose_name="Type de compte", choices=AccountTypes.choices)

    REQUIRED_FIELDS = [
        'first_name', 'last_name', 'email',
        'phone', 'adress', 'account_type'
    ]