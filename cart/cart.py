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

    def add(self, merch, merch_qty, merch_size):
        """
        Receives merch data from user button presses and adds them
        to the cart. Updating the cart by modifying the current user session,
        adds the price data from the merch item to the cart.
        """
        merch_id = merch.id
        if merch_id not in self.cart:
            self.cart[merch_id] = {"price": str(merch.price),
                                   "qty": int(merch_qty),
                                   "size": str(merch_size)}

        self.session.modified = True
