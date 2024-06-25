from django.db.models import Count, F
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser

from shop.models import Company, Product, Order, ProductOrder
from shop.serializers import (
    CompanySerializer,
    OrderSerializer,
    ProductSerializer,
    ProductImageSerializer,
    OrderRetrieveSerializer,
    ProductOrderSerializer
)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action == 'upload_image':
            return ProductImageSerializer
        return ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductOrderViewSet(viewsets.ModelViewSet):
    queryset = ProductOrder.objects.all()
    serializer_class = ProductOrderSerializer
