# Generated by Django 4.2 on 2023-05-08 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_alter_order_total_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='size',
            field=models.CharField(default='L', max_length=2),
            preserve_default=False,
        ),
    ]
