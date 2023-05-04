from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from store.models import Merch
from .cart import Cart

# Create your views here.


def cart_summary(request):
    """A view to show the carts content"""
    return render(request, "cart/cart.html")


def cart_add(request):
    """A view to collect ajax data when an item
    is added to the cart via a button press by the user"""
    cart = Cart(request)
    if request.POST.get("action") == "add_to_cart":
        merch_id = str(request.POST.get("merchid"))
        merch_qty = int(request.POST.get("merchqty"))
        merch_size = str(request.POST.get("merchsize"))
        merch = get_object_or_404(Merch, id=merch_id)
        cart.add(merch=merch, merch_qty=merch_qty, merch_size=merch_size)
        response = JsonResponse({"qty": merch_qty})
        return response
