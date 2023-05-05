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
        merch_id = merch.id
        if merch_id not in self.cart:
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

    def delete(self, merch):
        """Removes an item from the cart/session data."""
        merch_id = str(merch)  # made a string in views
        if merch_id in self.cart:
            del self.cart[merch_id]

        self.session.modified = True

    def update(self, merch, qty, size):
        """Updates items in the cart/session data."""
        merch_id = str(merch)

        if merch_id in self.cart:
            self.cart[merch_id]["qty"] = qty
            self.cart[merch_id]["size"] = size

        self.save()

    def save(self):
        """Saves the cart session."""
        self.session.modified = True
