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

        self.session.modified = True

    def __len__(self):
        """Count quantity of items within the cart."""
        return sum(item["qty"] for item in self.cart.values())
