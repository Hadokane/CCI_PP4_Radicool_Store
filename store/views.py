from django.shortcuts import render, get_object_or_404
from .models import Category, Collection, Merch

# Create your views here.


def categories(request):
    return {"categories": Category.objects.all()}


def collections(request):
    return {"collections": Collection.objects.all()}


def home(request):
    return render(request, "store/home.html", {"merch": Merch.objects.all()})


def merch_info(request, slug):
    merch = get_object_or_404(Merch, slug=slug, in_stock=True)
    return render(request, "store/merch/info.html", {"merch": merch})
