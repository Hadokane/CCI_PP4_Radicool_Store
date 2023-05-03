from django.contrib import admin
from .models import Category, Collection, Merch

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["cat_name", "slug"]
    # defaults slug to the cat_name
    prepopulated_fields = {"slug": ("cat_name",)}
    # orders the view
    ordering = ("cat_name",)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["col_name", "slug"]
    # defaults slug to the col_name
    prepopulated_fields = {"slug": ("col_name",)}
    # orders the view
    ordering = ("col_name",)


@admin.register(Merch)
class MerchAdmin(admin.ModelAdmin):
    list_display = [
        "product_name", "slug", "description", "price", "category",
        "collection", "image", "created",]
    list_filter = [
        "category", "collection", "product_name", "slug", "price",]
    list_editable = [
        "description", "price", "category", "collection", "image",]
    # defaults slug to the product_name
    prepopulated_fields = {"slug": ("product_name",)}
    # orders the view
    ordering = ("product_name",)
