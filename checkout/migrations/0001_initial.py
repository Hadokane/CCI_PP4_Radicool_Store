# Generated by Django 4.2 on 2023-05-08 12:26

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0005_alter_merch_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(editable=False, max_length=32)),
                ('full_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('street_address_1', models.CharField(max_length=80)),
                ('street_address_2', models.CharField(blank=True, max_length=80, null=True)),
                ('town_or_city', models.CharField(max_length=40)),
                ('county', models.CharField(blank=True, max_length=80, null=True)),
                ('postcode', models.CharField(blank=True, max_length=20, null=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('order_total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('delivery_cost', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('grand_total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(blank=True, max_length=2, null=True)),
                ('quantity', models.IntegerField(default=0)),
                ('item_total', models.DecimalField(decimal_places=2, editable=False, max_digits=11)),
                ('merch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.merch')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_item', to='checkout.order')),
            ],
        ),
    ]
