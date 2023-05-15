from radicool import settings
from .models import Merch


def wishlist_context(request):
    """If user is signed_in add to wish list works.
    Otherwise allauth redirects the user to sign in."""
    if request.user.is_authenticated:
        wishlist = Merch.objects.filter(user_wishlist=request.user)
        return ({"wishlist": wishlist})
