from django.shortcuts import render, redirect, reverse
from .forms import OrderForm


def checkout(request):
    order_form = OrderForm()
    context = {
        "order_form": order_form,
    }
    return render(request, "checkout/checkout.html", context)
