# Generated by Django 4.2 on 2023-05-08 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_number',
            field=models.CharField(default=2222222222222222222333333, editable=False, max_length=32),
            preserve_default=False,
        ),
    ]
