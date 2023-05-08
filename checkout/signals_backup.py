from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Order, OrderItem


@receiver(post_save, sender=OrderItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Receives signals from created orderitem
    and updates the order total
    """
    instance.order.update_total()


@receiver(post_delete, sender=OrderItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Updates the order total on orderitem delete
    """
    instance.order.update_total()
