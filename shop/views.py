from django.db.models import Count, F
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from shop.models import Company, Product, Order, ProductOrder
from shop.permissions import permissions_read_if_anonymous
from shop.serializers import (
    CompanySerializer,
    OrderSerializer,
    OrderListRetrieveSerializer,
    ProductSerializer,
    ProductImageSerializer,
    ProductOrderSerializer,
    ProductListSerializer,
)


class DefaultSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "size"
    max_page_size = 100


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_permissions(self):
        return permissions_read_if_anonymous(self)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    pagination_class = DefaultSetPagination

    def get_permissions(self):
        return permissions_read_if_anonymous(self)

    def get_serializer_class(self):
        if self.action == "upload_image":
            return ProductImageSerializer
        elif self.action == "list":
            return ProductListSerializer
        return ProductSerializer

    @staticmethod
    def _params_to_ints(qs):
        return tuple(int(str_id) for str_id in qs.split(","))

    def get_queryset(self):
        queryset = self.queryset

        company = self.request.query_params.get("company")
        if company:
            company = self._params_to_ints(company)
            queryset = queryset.filter(company_id__in=company)

        if self.action in ("list", "retrieve"):
            queryset = queryset.prefetch_related("company")

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "full_name",
                type={"type": "string"},
                description="Company and Product name",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = DefaultSetPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)

        if self.action == "list":
            queryset = queryset.prefetch_related("product_orders__product")

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action in ("list", "retrieve"):
            serializer = OrderListRetrieveSerializer
        return serializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "subtotal",
                type={"type": "float"},
                description="Subtotal of the product",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


class ProductOrderViewSet(viewsets.ModelViewSet):
    queryset = ProductOrder.objects.all()
    serializer_class = ProductOrderSerializer
