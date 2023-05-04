from django.urls import path
from . import views

# links to the namespace specified in radicool/urls
app_name = "cart"

urlpatterns = [
    path('', views.cart_summary, name='cart_summary'),
    path('add/', views.cart_add, name='cart_add'),
]
