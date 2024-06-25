from django.db import transaction
from rest_framework import serializers

from shop.models import Product, Company, Order, ProductOrder


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "name",


class ProductSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Product
        fields = (
            "name", "type_product", "company", "price", "capacity",
            "output", "cycle_life", "created_at", "image"
        )


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("name", "image")


class OrderRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order


class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = ("order", "product", "price")
        read_only_fields = ("price",)


class OrderSerializer(serializers.ModelSerializer):
    product_orders = ProductOrderSerializer(many=True, allow_empty=False, source='productorder_set')

    class Meta:
        model = Order
        fields = ("product_orders", "user", "created_at")
        read_only_fields = ("user", "created_at")

    def create(self, validated_data):
        product_orders_data = validated_data.pop('product_orders')
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            for product_order_data in product_orders_data:
                ProductOrder.objects.create(order=order, **product_order_data)
            return order

