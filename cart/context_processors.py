from .cart import Cart


# Cart data is requested and returned. Sessions.
def cart(request):
    return {"cart": Cart(request)}
