from django.urls import path
from . import views

# links to the namespace specified in radicool/urls
app_name = "profiles"

urlpatterns = [
    path('', views.profile, name='profile'),
]
