from django.shortcuts import render, reverse, get_object_or_404, redirect
from .models import Category, Collection, Merch
from store.forms import MerchSearchForm

# Create your views here.


# Show all Categories in navbar.
def categories(request):
    return {"categories": Category.objects.all()}


# Show all Collections in navbar.
def collections(request):
    return {"collections": Collection.objects.all()}


# Show a selection of Merchandise. Acts as Site Index/Homepage.
def home(request):
    """A view to act as the sites homepage"""
    return render(request, "store/home.html",
                  {"merch": Merch.objects.filter(hot_item=True)})


# Show all Merchandise in the store.
def all_products(request):
    """A view to show all available products"""

    merch = Merch.objects.all()
    sort = None
    direction = None
    current_sorting = None

    if "sort" in request.GET:
        sortkey = request.GET["sort"]
        sort = sortkey

        if sortkey == "name":
            sortkey = "lower_name"
            merch = merch.annotate(lower_name=Lower("name"))

        if "direction" in request.GET:
            direction = request.GET['direction']
            if direction == "desc":
                sortkey = f"-{sortkey}"
        merch = merch.order_by(sortkey)

        current_sorting = f"{sort}_{direction}"

    return render(request, "store/products.html",
                  {"merch":  merch,
                   "current_sorting": current_sorting})


# Search for specific Merchandise within the store.
def merch_search(request):
    """A view to handle product searches"""
    form = MerchSearchForm

    # Initialise the results field
    results = []
    q = ""

    # Check the search is valid and pass it through
    if "q" in request.GET:
        form = MerchSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data["q"]

            # filter Merch table, checks description & names
            results = Merch.objects.filter(
                product_name__icontains=q) | Merch.objects.filter(
                    description__icontains=q)

    return render(request, "store/search.html", {
        "form": form,
        "results": results,
        "q": q})


# Show specific Merch info, if in_stock.
def merch_info(request, slug):
    """A view shown when an individual piece of merchandise is selected."""
    merch = get_object_or_404(Merch, slug=slug, in_stock=True)
    return render(request, "store/merch/info.html", {"merch": merch})


# Show specific Category of Merch.
def category_info(request, category_slug):
    """A view shown when an individual category is selected."""
    category = get_object_or_404(Category, slug=category_slug)
    merch = Merch.objects.filter(category=category)
    return render(request, "store/merch/category.html",
                  {"category": category, "merch": merch})


# Show specific Collection of Merch.
def collection_info(request, collection_slug):
    """A view shown when an individual collection is selected."""
    collection = get_object_or_404(Collection, slug=collection_slug)
    merch = Merch.objects.filter(collection=collection)
    return render(request, "store/merch/collection.html",
                  {"collection": collection, "merch": merch})
