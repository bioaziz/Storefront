from tags.models import TaggedItem
from django.contrib import admin, messages
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models


class InventoryFilter(admin.SimpleListFilter):
    title = 'Inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),
            ('<20', 'Medium'),
            ('>20', 'High'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        elif self.value() == '<20':
            return queryset.filter(inventory__gte=10, inventory__lt=20)
        elif self.value() == '>20':
            return queryset.filter(inventory__gt=20)


# Register your models here.

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = ['promotions']
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['collection']
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory', 'inventory_status', 'collection_title']
    list_per_page = 20
    search_fields = ['title']
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_editable = ['inventory', 'unit_price']
    list_select_related = ['collection']

    def collection_title(self, product: object) -> object:
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        elif product.inventory < 20:
            return 'Medium'
        return 'High'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} inventory items cleared',
            messages.WARNING
        )


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    list_per_page = 20
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (reverse("admin:store_product_changelist")
               + '?'
               + urlencode({
                    'collection__id': collection.id,
                }))
        return format_html('<a href="{}" >{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'full_name', 'membership', 'orders']
    list_editable = ['membership']
    ordering = ('first_name', 'last_name')
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    def full_name(self, customer: object) -> str:
        return f'{customer.first_name} {customer.last_name}'

    @admin.display(ordering='orders')
    def orders(self, customer: models.Customer):
        url = (reverse("admin:store_customer_changelist")
               + "?"
               + urlencode({
                    'customer__id': str(customer.id)
                })
               )
        return format_html('<a href={}>{} Orders</>', url, customer.orders)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders=Count('order')
        )
    # @admin.display(ordering='orders_count')
    # def orders(self, customer):
    #     url = (
    #         reverse('admin:store_order_changelist')
    #         + '?'
    #         + urlencode({
    #             'customer__id': str(customer.id)
    #         }))
    #     return format_html('<a href="{}">{} Orders</a>', url, customer.orders_count)
    #
    # def get_queryset(self, request):
    #     return super().get_queryset(request).annotate(
    #         orders_count=Count('order')
    #     )


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    min_num = 1
    max_num = 10
    autocomplete_fields = ['product']


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id', 'placed_at', 'customer']
