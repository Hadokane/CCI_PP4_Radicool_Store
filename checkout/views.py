import os  # for secret stripe key
import json
import stripe
from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .forms import OrderForm
from cart.cart import Cart


def checkout(request):
    order_form = OrderForm()

    cart = Cart(request)
    total = str(cart.get_total_price())
    total = total.replace(".", "")
    total = int(total)  # converts price to int for stripe use

    # creates stripe payment intent
    stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency="gbp",
    )

    print(intent)

    context = {
        "order_form": order_form,
        "client_secret": intent.client_secret,
        "stripe_public_key": "pk_test_51N2tqaJBncpFz3JEf8j2jpgwSCe7Y36AB196lDJFNi90ewcVMvhtltqiD6pF8xuMpD44VTahBu5lGUXZGU8EhAcw00rgFnAqNO",
    }
    return render(request, "checkout/checkout.html", context)
