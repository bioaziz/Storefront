from django.contrib import admin
from django.contrib.admin import TabularInline
from django.contrib.contenttypes.admin import GenericTabularInline

from store.models import Product
from tags.models import TaggedItem
from store.admin import ProductAdmin


# Register your models here.

class TagInLine(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ['tag']

class CustomProductAdmin(ProductAdmin):
    inlines = [TagInLine]
    search_fields = ['tag']

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)