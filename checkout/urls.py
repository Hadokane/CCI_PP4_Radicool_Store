from django.urls import path
from . import views

# links to the namespace specified in radicool/urls
app_name = "checkout"

urlpatterns = [
    path('', views.checkout, name="checkout")
]
