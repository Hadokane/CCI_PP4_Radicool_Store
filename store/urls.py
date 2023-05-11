from django.urls import path
from . import views

# links to the namespace specified in radicool/urls
app_name = "store"

urlpatterns = [
    # Home view
    path("", views.home, name="home"),
    # all products view
    path("products/", views.all_products, name="products"),
    # search products view
    path("search/", views.merch_search, name="search"),
    # used to generate urls, reads the models slug
    path("<slug:slug>", views.merch_info, name="merch_info"),
    # used to generate urls, reads the models slug
    path("cat/<slug:category_slug>", views.category_info,
         name="category_info"),
    # used to generate urls, reads the models slug
    path("col/<slug:collection_slug>", views.collection_info,
         name="collection_info"),
    # used to add products if an admin
    path('add/', views.add_merch, name='add_merch'),
    path('edit/<int:merch_id>/', views.edit_merch, name='edit_merch'),
    path('delete/<int:merch_id>/',
         views.delete_merch, name='delete_merch'),
]
