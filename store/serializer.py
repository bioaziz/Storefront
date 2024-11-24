from decimal import Decimal
from rest_framework import serializers
from store.models import Product, Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']
        depth = 2

    products_count = serializers.IntegerField()


class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField(method_name='get_price_with_tax')
    price = serializers.DecimalField(max_digits=10, decimal_places=2, source='unit_price')

    class Meta:
        model = Product
        fields = ['title', 'slug', 'description', 'price', 'inventory', 'price_with_tax', 'collection']
        depth = 0

    @staticmethod
    def get_price_with_tax(obj: Product):
        new_price = obj.unit_price * Decimal(1.1)
        return new_price
