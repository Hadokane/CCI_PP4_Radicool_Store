import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from django_countries.fields import CountryField
from store.models import Merch


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    street_address_1 = models.CharField(max_length=80, null=False, blank=False)
    street_address_2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    county = models.CharField(max_length=80, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2,
                                        null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    original_cart = models.TextField(null=False, blank=False, default='')

    def _generate_order_number(self):
        """ Used to generates unique order numbers. 32 Character string."""
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a single item is added,
        accounting for delivery costs.
        """
        self.order_total = self.order_item.aggregate(
            Sum('item_total'))['item_total__sum'] or 0
        self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        If no order number is set, this overrides it and generates one.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("date",)

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE, blank=False,
                              related_name='order_item', null=False)
    merch = models.ForeignKey(Merch,
                              on_delete=models.CASCADE)
    size = models.CharField(max_length=2)
    quantity = models.IntegerField(default=0)
    item_total = models.DecimalField(max_digits=11, decimal_places=2,
                                     editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the item total
        and update the order total.
        """
        self.item_total = self.merch.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.merch.product_name} on order {self.order.order_number}'
