from django.urls import path
from . import views
from .webhooks import stripe_webhook

# links to the namespace specified in radicool/urls
app_name = "checkout"

urlpatterns = [
    path('', views.checkout, name="checkout"),
    path('checkout_success/<order_number>',
         views.checkout_success, name="checkout_success"),
    path('cache_checkout_data/',
         views.cache_checkout_data, name="cache_checkout_data"),
    path('webhook/', stripe_webhook, name="stripe_webhook"),
]
