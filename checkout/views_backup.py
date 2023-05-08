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

    if request.method == 'POST':
        cart = Cart(request)
        total = cart.get_total_price()

        form_data = {
                'full_name': request.POST['full_name'],
                'email': request.POST['email'],
                'town_or_city': request.POST['town_or_city'],
                'street_address_1': request.POST['street_address_1'],
                'street_address_2': request.POST['street_address_2'],
                'county': request.POST['county'],
                'postcode': request.POST['postcode'],
                'country': request.POST['country'],
            }
        order_form = OrderForm(form_data)

        if order_form.is_valid():
            order = order_form.save()
            for item in cart:
                order_item = OrderItem(
                        order=Order.id,
                        size=item["size"],
                        quantity=item["qty"],
                        item_total=item["total_price"],
                    )
                merch_ids = cart.cart.keys()
                products = Merch.objects.filter(id__in=merch_ids)

                for p in products:
                    order_item = OrderItem(
                        merch=p
                    )
                    print("MERCH:" + str(p))
                    print("ORDER:" + str(order))
                    print("Size:" + str(item["size"]))
                    print("QTY:" + str(item["qty"]))
                    order_item.save()

            request.session["save_info"] = "save_info" in request.POST
            return redirect(reverse("checkout:checkout_success", args=[order.order_number]))

    else:
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

        order_form = OrderForm()
        template = 'checkout/checkout.html'
        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
        }

        return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if 'cart' in request.session:
        del request.session['cart']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
