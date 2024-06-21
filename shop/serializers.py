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


class OrderSerializer(serializers.ModelSerializer):
    products_in_order = ProductSerializer(many=True, read_only=True, allow_empty=False)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("created_at", "subtotal")

    def create(self, validated_data):
        with transaction.atomic():
            products = validated_data.pop('order_products')
            order = Order.objects.create(**validated_data)
            for product_data in products:
                ProductOrder.objects.create(order=order, **product_data)
            return order


class OrderRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


# class OrderProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderProduct
#         fields = (
#             "name", "type_product", "company", "price", "capacity",
#             "output", "cycle_life", "created_at", "image", "order"
#         )
