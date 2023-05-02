from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    cat_name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)  # Creates URL

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.cat_name  # Returns the cat_name


class Collection(models.Model):
    col_name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)  # Creates URL

    class Meta:
        verbose_name_plural = "Collections"

    def __str__(self):
        return self.col_name  # Returns the col_name


class Merch(models.Model):
    product_name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category, related_name="product_cat", on_delete=models.CASCADE,)
    collection = models.ForeignKey(
        Collection, related_name="product_col", on_delete=models.CASCADE,
        blank=True, null=True)
    image = models.ImageField(
        upload_to='images/', default='images/placeholder')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Merch"
        ordering = ("-created",)

    def __str__(self):
        return self.product_name  # Returns the cat_name
