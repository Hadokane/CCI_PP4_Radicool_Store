import os
import json
import stripe
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .forms import OrderForm
from cart.cart import Cart
from cart.context_processors import cart
from store.models import Merch
from .models import OrderItem, Order


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    if os.path.exists("env.py"):
        import env
        STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
        stripe_secret_key = STRIPE_SECRET_KEY

    cart = Cart(request)
    if not cart:
        return redirect(reverse('store:products'))

    current_cart = Cart(request)
    total = current_cart.get_total_price()
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )
    print(intent)

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)
