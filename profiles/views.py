from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from checkout.models import Order, OrderItem
from store.models import Merch
from .models import UserProfile
from .forms import UserProfileForm


@login_required
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated!")

    form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        "form": form,
        "profile": profile,
        "orders": orders,
        }

    return render(request, template, context)


def order_history(request, order_number):
    """Display past orders"""
    order = get_object_or_404(Order, order_number=order_number)

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)


@login_required
def wishlist(request):
    """Displays the users wishlist"""
    merch = Merch.objects.filter(user_wishlist=request.user)
    return render(
        request,
        "profiles/wishlist.html",
        {"wishlist": merch}
        )


@login_required
def update_wishlist(request, id):
    """Add/Remove items from the users wishlist"""
    merch = get_object_or_404(Merch, id=id)
    # if on users list, remove the item
    if merch.user_wishlist.filter(id=request.user.id).exists():
        merch.user_wishlist.remove(request.user)
        messages.success(
            request,
            merch.product_name
            + " has been removed from your WishList")
    # if not on users list, add the item
    else:
        merch.user_wishlist.add(request.user)
        messages.success(
            request,
            "Added "
            + merch.product_name
            + " to your WishList")
    # sends data back to the same html page
    return HttpResponseRedirect(request.META["HTTP_REFERER"])
