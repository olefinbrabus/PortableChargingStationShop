from django.db import transaction
from django.db.models import UniqueConstraint
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
        validators = [
            UniqueConstraint(
                fields=('name', 'type_product'),
                name='unique_product_name_type'
            ),
        ]


class ProductListSerializer(ProductSerializer):
    class Meta:
        model = Product
        fields = ('full_name', 'image')


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("name", "image")


class OrderRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order


class ProductOrderSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = ProductOrder
        fields = ("order", "product", "price")
        read_only_fields = ("price",)


class OrderSerializer(serializers.ModelSerializer):
    product_orders = ProductOrderSerializer(many=True, allow_empty=False, read_only=False)

    class Meta:
        model = Order
        fields = ("created_at", "subtotal", "product_orders")
        read_only_fields = ("created_at",)

    def create(self, validated_data):
        print(validated_data)
        product_orders_data = validated_data.pop('product_orders')

        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            for product_order_data in product_orders_data:
                ProductOrder.objects.create(order=order, **product_order_data)
            return order


class OrderListSerializer(OrderSerializer):
    product_orders = ProductOrderSerializer(many=True, read_only=True,)
