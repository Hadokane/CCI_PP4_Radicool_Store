from radicool import settings
from store.models import Merch
from decimal import Decimal


class Cart():
    """
    A base Cart class, provides default behaviours that
    can be inherited or overridden, as required. Used to
    store information for user sessions.
    """

    def __init__(self, request):

        self.session = request.session
        cart = self.session.get('session_key')
        # if no session exists, create session
        if "session_key" not in request.session:
            cart = self.session["session_key"] = {}
        # show stored session cart
        self.cart = cart

    def add(self, merch, qty, size):
        """
        Receives merch data from user button presses and adds them
        to the cart. Updating the cart by modifying the current user session,
        adds the price data from the merch item to the cart.
        """
        merch_id = str(merch.id)

        if merch_id in self.cart:
            self.cart[merch_id]["qty"] = qty  # if qty exists, update it
        else:
            self.cart[merch_id] = {"price": str(merch.price),
                                   "qty": int(qty),
                                   "size": str(size)}

        self.save()

    def __iter__(self):
        """
        Creates an iterable class for this object.
        Collects merch_id in session data, queries database,
        returns item matches for cart to display.
        """
        merch_ids = self.cart.keys()  # gets keys from add
        products = Merch.objects.filter(id__in=merch_ids)  # filters model
        cart = self.cart.copy()  # copies session data of the cart

        for product in products:
            cart[str(product.id)]["product"] = product  # adds full model data

        for item in cart.values():
            item["price"] = Decimal(item["price"])  # makes price a decimal
            item["total_price"] = item["price"] * item["qty"]  # calculation
            yield item  # shows the final item

    def __len__(self):
        """Count quantity of items within the cart."""
        return sum(item["qty"] for item in self.cart.values())

    def get_total_price(self):
        """Calculates the total price of all items."""
        return sum(Decimal(item["price"]) * item[
            "qty"] for item in self.cart.values())

    # Calculate the shipping
    def delivery_context(self):
        """Calculates the delivery cost of the order."""
        total = self.get_total_price()
        if total < settings.FREE_DELIVERY_THRESHOLD:
            delivery = Decimal(settings.STANDARD_DELIVERY_COST)
            free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
        else:
            delivery = 0
            free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total

        grand_total = delivery + total

        context = {
            "total": total,
            "delivery": delivery,
            "free_delivery_delta": free_delivery_delta,
            "free_delivery_threshold": settings.FREE_DELIVERY_THRESHOLD,
            "grand_total": grand_total,
        }
        return context

    # Get the shipping cost
    def get_delivery_cost(self):
        """Calculates the delivery cost of the order."""
        total = self.get_total_price()
        if total < settings.FREE_DELIVERY_THRESHOLD:
            delivery = Decimal(settings.STANDARD_DELIVERY_COST)
            free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
        else:
            delivery = 0
            free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total

        grand_total = delivery + total

        return delivery

    # Calculate the grand total for Stripe use
    def grand_total(self):
        """Calculates the delivery cost of the order."""
        total = self.get_total_price()

        if total < settings.FREE_DELIVERY_THRESHOLD:
            delivery = Decimal(settings.STANDARD_DELIVERY_COST)
        else:
            delivery = 0

        grand_total = delivery + total

        return grand_total

    def delete(self, merch):
        """Removes an item from the cart/session data."""
        merch_id = str(merch)  # made a string in views
        if merch_id in self.cart:
            del self.cart[merch_id]

        self.session.modified = True

    def update(self, merch, qty, size, itemprice):
        """Updates items in the cart/session data."""
        merch_id = str(merch)

        if merch_id in self.cart:
            self.cart[merch_id]["qty"] = qty
            self.cart[merch_id]["size"] = size

        self.save()

    def save(self):
        """Saves the cart session."""
        self.session.modified = True

    def clear(self):
        del self.session["session_key"]
        self.save()
