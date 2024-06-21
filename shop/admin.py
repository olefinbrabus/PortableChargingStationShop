from django.contrib import admin

from shop.models import Company, Product, Order, ProductOrder


class OrderProductInline(admin.TabularInline):
    model = ProductOrder
    extra = 1
    readonly_fields = ('price',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', 'subtotal')}),
    )
    readonly_fields = ('subtotal',)
    inlines = OrderProductInline,


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
    # fieldsets = (
    #     (None, {'fields': ('product', 'price')}),
    # )


admin.site.register(Company)


