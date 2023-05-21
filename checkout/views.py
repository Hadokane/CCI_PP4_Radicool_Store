import stripe
import uuid

from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse)
from django.conf import settings
from django.views.decorators.http import require_POST
from django.contrib import messages

from .forms import OrderForm
from cart.cart import Cart
from .models import Order, OrderItem
from profiles.models import UserProfile
from profiles.forms import UserProfileForm


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
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
        cartdelivery = cart.get_delivery_cost()
        cartgrand = cart.grand_total()
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
                total_delivery_cost=cartdelivery,
                total_grand=cartgrand,
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
        total = current_cart.grand_total()
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key

        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
            metadata={"userid": request.user.id},
        )

        # Attempt to prefill the form with any info
        # the user maintains in their profile
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.default_full_name,
                    'email': profile.user.email,
                    'street_address_1': profile.default_street_address_1,
                    'street_address_2': profile.default_street_address_2,
                    'town_or_city': profile.default_town_or_city,
                    'county': profile.default_county,
                    'postcode': profile.default_postcode,
                    'country': profile.default_country,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
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

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        # Show confirmation message
        messages.success(request, f"Order: {order_number} successful! \
                     Confirmation Email sent to {order.email}.")

        # Save the user's info
        if save_info:
            profile_data = {
                "default_full_name": order.full_name,
                'default_street_address_1': order.street_address_1,
                'default_street_address_2': order.street_address_2,
                'default_town_or_city': order.town_or_city,
                'default_county': order.county,
                'default_postcode': order.postcode,
                'default_country': order.country,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    cart = Cart(request)
    cart.clear()

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)


def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)
