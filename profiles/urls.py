from django.urls import path
from . import views

# links to the namespace specified in radicool/urls
app_name = "profiles"

urlpatterns = [
    path('', views.profile, name='profile'),
    path('order_history/<order_number>',
         views.order_history,
         name='order_history'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/update_wishlist/<int:id>',
         views.update_wishlist,
         name='update_wishlist'),
]
