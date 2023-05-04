from .cart import Cart
from decimal import Decimal
from django.conf import settings


# Cart data is requested and returned. Sessions.
def cart(request):
    return {"cart": Cart(request)}
