from django.contrib import admin

from app.models import (
    Order,
    OrderDetail,
    Product,
)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
        'stock',
    )
    search_fields = ('name',)


class OrderDetailAdmin(admin.StackedInline):
    model = OrderDetail
    extra = 1
    fk_name = 'order'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('date_time', 'get_total', 'get_total_usd')
    list_filter = ('date_time',)
    inlines = (OrderDetailAdmin,)
