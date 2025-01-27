# Generated by Django 5.1.4 on 2024-12-26 20:23

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('price', models.IntegerField()),
                ('description', models.CharField(max_length=300)),
                ('image', models.ImageField(upload_to='products/')),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('total_price', models.IntegerField()),
                ('payment_method', models.CharField(max_length=25)),
                ('state', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('phone', models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator('(01|05|07)[0-9]{8}$', message='Numéro de téléphone invalide')])),
                ('adress', models.CharField(blank=True, max_length=300, validators=[django.core.validators.MinLengthValidator(30, message="L'adresse doit contenir au moins 30 caractères")])),
                ('official_page', models.URLField(null=True, verbose_name='Page officielle')),
                ('is_online_only', models.BooleanField(default=False)),
                ('opening_time', models.TimeField()),
                ('closing_time', models.TimeField()),
                ('isActive', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('ordered_quantity', models.IntegerField()),
                ('total_price', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.product')),
            ],
        ),
    ]
