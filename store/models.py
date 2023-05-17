from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    cat_name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)  # Creates URL

    class Meta:
        verbose_name_plural = "Categories"

    def get_absolute_url(self):
        # Uses info on urls page to create dynamic link
        return reverse("store:category_info", args=[self.slug])

    def __str__(self):
        return self.cat_name  # Returns the cat_name


class Collection(models.Model):
    col_name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)  # Creates URL

    class Meta:
        verbose_name_plural = "Collections"

    def get_absolute_url(self):
        # Uses info on urls page to create dynamic link
        return reverse("store:collection_info", args=[self.slug])

    def __str__(self):
        return self.col_name  # Returns the col_name


class Merch(models.Model):
    product_name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    hot_item = models.BooleanField(default=False)
    category = models.ForeignKey(
        Category, related_name="product_cat", on_delete=models.SET_NULL,
        blank=True, null=True)
    collection = models.ForeignKey(
        Collection, related_name="product_col", on_delete=models.SET_NULL,
        blank=True, null=True)
    image = models.ImageField(
        upload_to='images/', default='static/logos/placeholder.jpg')
    created = models.DateTimeField(auto_now_add=True)
    user_wishlist = models.ManyToManyField(
        User, related_name="user_wishlist",
        blank="True")

    class Meta:
        verbose_name_plural = "Merch"
        ordering = ("-created",)

    def get_absolute_url(self):
        # Uses info on urls page to create dynamic link
        return reverse("store:merch_info", args=[self.slug])

    def __str__(self):
        return self.product_name  # Returns the cat_name
