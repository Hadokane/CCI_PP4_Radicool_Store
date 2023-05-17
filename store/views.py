from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Category, Collection, Merch
from .forms import MerchSearchForm, MerchForm


# Show all Categories in navbar.
def categories(request):
    categories = Category.objects.all().order_by('cat_name')
    return {"categories": categories}


# Show all Collections in navbar.
def collections(request):
    return {"collections": Collection.objects.all().order_by('col_name')}


# Show a selection of Merchandise. Acts as Site Index/Homepage.
def home(request):
    """A view to act as the sites homepage"""

    if request.user.is_authenticated:
        wishlist = Merch.objects.filter(user_wishlist=request.user)
    else:
        wishlist = None

    return render(request, "store/home.html",
                  {"merch": Merch.objects.filter(hot_item=True),
                   "wishlist": wishlist})


# Show all Merchandise in the store.
def all_products(request):
    """
    A view to show all available products. Provides ordering buttons.
    """

    merch = Merch.objects.all()

    if request.user.is_authenticated:
        wishlist = Merch.objects.filter(user_wishlist=request.user)
    else:
        wishlist = None

    sort = None
    direction = None
    current_sorting = None

    if "sort" in request.GET:
        sortkey = request.GET["sort"]
        sort = sortkey

        if sortkey == "name":
            sortkey = "lower_name"
            merch = merch.annotate(lower_name=Lower("name"))
        # Allows names to appear in alphabetical order
        if sortkey == "category":
            sortkey = "category__cat_name"

        if sortkey == "collection":
            sortkey = "collection__col_name"

        # - reverses direction (ie: "z-a", "high-low")
        if "direction" in request.GET:
            direction = request.GET['direction']
            if direction == "desc":
                sortkey = f"-{sortkey}"
        merch = merch.order_by(sortkey)

        current_sorting = f"{sort}_{direction}"

    return render(request, "store/products.html",
                  {"merch":  merch,
                   "current_sorting": current_sorting,
                   "wishlist": wishlist})


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

            if request.user.is_authenticated:
                wishlist = Merch.objects.filter(user_wishlist=request.user)
            else:
                wishlist = None

    return render(request, "store/search.html", {
        "form": form,
        "results": results,
        "q": q,
        "wishlist": wishlist})


# Show specific Merch info, if in_stock.
def merch_info(request, slug):
    """A view shown when an individual piece of merchandise is selected."""
    merch = get_object_or_404(Merch, slug=slug, in_stock=True)

    if request.user.is_authenticated:
        wishlist = Merch.objects.filter(user_wishlist=request.user)
    else:
        wishlist = None

    return render(
        request,
        "store/merch/info.html",
        {"merch": merch,
         "wishlist": wishlist
         })


# Show specific Category of Merch.
def category_info(request, category_slug):
    """A view shown when an individual category is selected."""
    category = get_object_or_404(Category, slug=category_slug)
    merch = Merch.objects.filter(category=category)

    if request.user.is_authenticated:
        wishlist = Merch.objects.filter(user_wishlist=request.user)
    else:
        wishlist = None

    return render(request, "store/merch/category.html",
                  {"category": category, "merch": merch,
                   "wishlist": wishlist})


# Show specific Collection of Merch.
def collection_info(request, collection_slug):
    """A view shown when an individual collection is selected."""
    collection = get_object_or_404(Collection, slug=collection_slug)
    merch = Merch.objects.filter(collection=collection)

    if request.user.is_authenticated:
        wishlist = Merch.objects.filter(user_wishlist=request.user)
    else:
        wishlist = None

    return render(request, "store/merch/collection.html",
                  {"collection": collection, "merch": merch,
                   "wishlist": wishlist})


# Allows "BRAND" users to add merch
@login_required
def add_merch(request):
    """ Add a product to the store """

    if not User.objects.filter(
         pk=request.user.id, groups__name='Brand').exists():
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('store:home'))

    if request.method == 'POST':
        form = MerchForm(request.POST, request.FILES)
        if form.is_valid():
            merch = form.save()
            messages.success(request, 'Successfully added Merch!')
            return redirect(reverse('store:merch_info', args=[merch.slug]))
        else:
            messages.error(request,
                           ('Failed to add merch.'
                            'Please ensure the form is valid.'))
    else:
        form = MerchForm()

    template = 'superuser/add_merch.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


# Allows "BRAND" users to edit products
@login_required
def edit_merch(request, merch_id):
    """ Edit a product in the store """
    if not User.objects.filter(
         pk=request.user.id, groups__name='Brand').exists():
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('store:home'))

    merch = get_object_or_404(Merch, pk=merch_id)
    if request.method == 'POST':
        form = MerchForm(request.POST, request.FILES, instance=merch)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated merch!')
            return redirect(reverse('store:merch_info', args=[merch.slug]))
        else:
            messages.error(request,
                           ('Failed to update merch. '
                            'Please ensure the form is valid.'))
    else:
        form = MerchForm(instance=merch)
        messages.info(request, f'You are editing {merch.product_name}')

    template = 'superuser/edit_merch.html'
    context = {
        'form': form,
        'merch': merch,
    }

    return render(request, template, context)


# Allows "BRAND" users to delete products
@login_required
def delete_merch(request, merch_id):
    """ Delete a product from the store """
    if not User.objects.filter(
         pk=request.user.id, groups__name='Brand').exists():
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('store:home'))

    merch = get_object_or_404(Merch, pk=merch_id)
    merch.delete()
    messages.success(request, 'Merchandise deleted!')
    return redirect(reverse('store:products'))
