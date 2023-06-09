from django.db import models
from django_countries.fields import CountryField

from store.models import Merch
from profiles.models import UserProfile


class Order(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, null=False, blank=False)
    street_address_1 = models.CharField(max_length=250)
    street_address_2 = models.CharField(max_length=250)
    town_or_city = models.CharField(max_length=100)
    county = models.CharField(max_length=80)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=11, decimal_places=2)
    total_delivery_cost = models.DecimalField(max_digits=11, decimal_places=2)
    total_grand = models.DecimalField(max_digits=11, decimal_places=2)
    order_key = models.CharField(max_length=200)
    billing_status = models.BooleanField(default=False)
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="orders")

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return str(self.created)


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    merch = models.ForeignKey(Merch,
                              related_name='order_items',
                              on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=4)

    def __str__(self):
        return str(self.id)
