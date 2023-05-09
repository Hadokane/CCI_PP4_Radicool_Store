from django.contrib import admin
from .models import Order, OrderItem


class OrderItemAdminInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('price',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemAdminInline,)

    readonly_fields = ('order_key', "order_number", 'created', 'updated',
                       "total_paid",)

    fields = ('order_key', "order_number", 'created', 'updated',
              "full_name",
              'email', 'country',
              'postcode', 'town_or_city', 'street_address_1',
              'street_address_2', 'county',
              'total_paid', "billing_status",)

    list_display = ('order_key', "order_number", 'created', 'full_name',
                    'total_paid', "billing_status",)

    ordering = ('-created',)


admin.site.register(Order, OrderAdmin)
