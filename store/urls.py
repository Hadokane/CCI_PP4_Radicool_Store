from django.urls import path
from . import views

app_name = "store"  # links to the namespace specified in radicool/urls

urlpatterns = [
    path("", views.home, name="home")
]
