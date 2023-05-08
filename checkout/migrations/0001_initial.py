# Generated by Django 4.2 on 2023-05-08 14:48

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(editable=False, max_length=32)),
                ('full_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('street_address_1', models.CharField(max_length=250)),
                ('street_address_2', models.CharField(max_length=250)),
                ('town_or_city', models.CharField(max_length=100)),
                ('county', models.CharField(max_length=80)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('postcode', models.CharField(max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('total_paid', models.DecimalField(decimal_places=2, max_digits=5)),
                ('order_key', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=11)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('merch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='store.merch')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='checkout.order')),
            ],
        ),
    ]
