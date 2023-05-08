from django.contrib import admin
from .models import Order, OrderItem

admin.site.register(OrderItem)


class OrderItemAdminInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('price',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemAdminInline,)

    readonly_fields = ('order_key', 'created', 'updated',
                       "total_paid",)

    fields = ('order_key', 'created', 'updated',
              "full_name",
              'email', 'country',
              'postcode', 'town_or_city', 'street_address_1',
              'street_address_2', 'county',
              'total_paid',)

    list_display = ('order_key', 'created', 'full_name',
                    'total_paid',)

    ordering = ('-created',)


admin.site.register(Order, OrderAdmin)