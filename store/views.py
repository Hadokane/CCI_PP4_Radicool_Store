from django.shortcuts import render
from .models import Category, Collection, Merch

# Create your views here.


def home(request):
    products = Merch.objects.all()
    return render(request, "store/home.html", {"products": products})
