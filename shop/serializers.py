from django.db import transaction
from rest_framework import serializers

from shop.models import Product, Company, Order, ProductOrder


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("name",)


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            "name",
            "type_product",
            "company",
            "price",
            "capacity",
            "output",
            "cycle_life",
            "created_at",
            "image",
        )


class ProductListSerializer(ProductSerializer):
    full_name = serializers.CharField()

    class Meta:
        model = Product
        fields = (
            "full_name",
            "price",
            "image",
        )


class ProductRetrieveSerializer(ProductSerializer):
    company = CompanySerializer(read_only=True)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("name", "image")


class ProductOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductOrder
        fields = ("order", "product", "price")
        read_only_fields = ("price",)


class ProductOrderListSerializer(ProductOrderSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = ProductOrder
        fields = ("product", "price")
        read_only_fields = ("price",)


class OrderSerializer(serializers.ModelSerializer):
    product_orders = ProductOrderSerializer(many=True, allow_empty=False)
    subtotal = serializers.FloatField(read_only=True)

    class Meta:
        model = Order
        fields = ("created_at", "subtotal", "product_orders")
        read_only_fields = ("created_at", "subtotal")

    def create(self, validated_data):
        print(validated_data)
        product_orders_data = validated_data.pop("product_orders")

        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            for product_order_data in product_orders_data:
                ProductOrder.objects.create(order=order, **product_order_data)
            return order


class OrderRetrieveSerializer(OrderSerializer):
    product_orders = ProductOrderSerializer(
        many=True,
        read_only=True,
    )


class OrderListSerializer(OrderSerializer):
    product_orders = ProductOrderListSerializer(many=True)
