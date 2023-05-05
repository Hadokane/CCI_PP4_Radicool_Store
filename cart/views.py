from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from store.models import Merch
from .cart import Cart
from decimal import Decimal


def cart_summary(request):
    """A view to show the carts content"""
    cart = Cart(request)
    return render(request, "cart/cart.html", {"cart": cart})


def cart_add(request):
    """
    Collects jSon data when an item is added to the cart,
    via a button press by the user.
    Gathers the id, qty and size, compares with database.
    Adds to the session.
    """
    cart = Cart(request)
    if request.POST.get("action") == "add_to_cart":
        # Variables for cart.add function
        merch_id = str(request.POST.get("merchid"))
        merch_qty = int(request.POST.get("merchqty"))
        merch_size = str(request.POST.get("merchsize"))
        merch = get_object_or_404(Merch, id=merch_id)
        # Run the cart.add function
        cart.add(merch=merch, qty=merch_qty, size=merch_size)
        # Returns total quantity to the cart on the front end.
        cart_qty = cart.__len__()
        response = JsonResponse({"qty": cart_qty})
        return response


def cart_delete(request):
    """
    Removes Items from the cart.
    Deletes an item, gets the cart quantity, calculates the total price.
    Updates the fields.
    """
    cart = Cart(request)
    if request.POST.get("action") == "delete":
        merch_id = str(request.POST.get("merchid"))
        cart.delete(merch=merch_id)

        cart_qty = cart.__len__()
        cart_total = cart.get_total_price()

        response = JsonResponse({"qty": cart_qty,
                                 "subtotal": cart_total})
        return response


def cart_update(request):
    """
    Updates Items within the cart.
    Gets the id, qty and size. Updates the cart.
    Calculates the total price.
    """
    cart = Cart(request)
    if request.POST.get("action") == "update":
        merch_id = str(request.POST.get("merchid"))
        merch_qty = int(request.POST.get("merchqty"))
        merch_size = str(request.POST.get("merchsize"))
        item_price = str(request.POST.get("itemprice"))
        cart.update(merch=merch_id, qty=merch_qty, size=merch_size,
                    itemprice=item_price)

        item_total = Decimal(item_price)*int(merch_qty)  # calc item total

        cart_qty = cart.__len__()
        cart_total = cart.get_total_price()  # calc cart total

        response = JsonResponse({"qty": cart_qty,
                                 "subtotal": cart_total,
                                 "size": merch_size,
                                 "itemqty": merch_qty,
                                 "itemtotal": item_total
                                 })
        return response
