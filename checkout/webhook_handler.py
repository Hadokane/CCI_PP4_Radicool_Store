from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderItem
from store.models import Merch
from profiles.models import UserProfile

import stripe
import json
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        customers_email = order.email
        subject = render_to_string(
            '../templates/emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            '../templates/emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [customers_email]
        )

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        cart = intent.metadata.cart

        # Get the Charge object
        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )

        billing_details = stripe_charge.billing_details  # updated
        shipping_details = intent.shipping
        grand_total = round(stripe_charge.amount / 100, 2)  # updated

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address_1__iexact=shipping_details.address.line1,
                    street_address_2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    total_grand=grand_total,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]}'
                        '| SUCCESS: Verified order already in database',
                status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    user_profile=profile,
                    email=billing_details.email,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address_1=shipping_details.address.line1,
                    street_address_2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                )
                for item_id, item_data in json.loads(cart).items():
                    merch = Merch.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderItem(
                            order=order,
                            merch=merch,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data[
                         'items_by_size'].items():
                            order_line_item = OrderItem(
                                order=order,
                                merch=merch,
                                quantity=quantity,
                                size=size,
                            )
                            order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        self._send_confirmation_email(order)
        return HttpResponse(
            content=(f'Webhook received: {event["type"]} | SUCCESS: '
                     'Created order in webhook'),
            status=200)

    def handle_payment_intent_created(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        self._send_confirmation_email(order)
        return HttpResponse(
            content=(f'Webhook received: {event["type"]}'),
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
