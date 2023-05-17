# Generated by Django 4.2 on 2023-05-08 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                (
                    'id', models.BigAutoField(
                        auto_created=True, primary_key=True,
                        serialize=False, verbose_name='ID')),
                ('cat_name', models.CharField(db_index=True, max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID')),
                ('col_name', models.CharField(db_index=True, max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Collections',
            },
        ),
        migrations.CreateModel(
            name='Merch',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('in_stock', models.BooleanField(default=True)),
                ('hot_item', models.BooleanField(default=False)),
                ('image', models.ImageField(
                    default='images/placeholder.jpg', upload_to='images/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='product_cat', to='store.category')),
                ('collection', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='product_col', to='store.collection')),
            ],
            options={
                'verbose_name_plural': 'Merch',
                'ordering': ('-created',),
            },
        ),
    ]
