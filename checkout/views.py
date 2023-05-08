import os
import json
import stripe
import uuid

from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse)
from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import OrderForm
from cart.cart import Cart
from cart.context_processors import cart
from store.models import Merch
from .models import Order, OrderItem


@require_POST
def cache_checkout_data(request):
    try:
        cart = Cart(request)
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, ('Sorry, your payment cannot be '
                                 'processed right now. Please try '
                                 'again later.'))
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        cart = Cart(request)
        carttotal = cart.get_total_price()
        user_id = request.user.id
        num = uuid.uuid4().hex.upper()

        order = Order.objects.create(
                full_name=request.POST["full_name"],
                email=request.POST['email'],
                town_or_city=request.POST['town_or_city'],
                street_address_1=request.POST['street_address_1'],
                street_address_2=request.POST['street_address_2'],
                county=request.POST['county'],
                postcode=request.POST['postcode'],
                country=request.POST['country'],
                total_paid=carttotal,
                order_key=request.POST.get('client_secret'),
                order_number=num,
                )
        order_id = order.pk

        for item in cart:
            OrderItem.objects.create(
                    order_id=order_id,
                    merch=item['product'],
                    price=item['price'],
                    quantity=item['qty'],
                    size=item["size"],
                    )

        return redirect(reverse("checkout:checkout_success",
                        args=[order.order_number]))

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
            metadata={"userid": request.user.id},
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
