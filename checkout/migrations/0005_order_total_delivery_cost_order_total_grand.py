# Generated by Django 4.2 on 2023-05-12 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_alter_orderitem_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_delivery_cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=11),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='total_grand',
            field=models.DecimalField(decimal_places=2, default=3000, max_digits=11),
            preserve_default=False,
        ),
    ]
