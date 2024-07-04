from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from shop.models import Company, Product, Order, ProductOrder
from shop.permissions import IsAdminOrReadOnly
from shop.serializers import (
    CompanySerializer,
    OrderSerializer,
    OrderRetrieveSerializer,
    OrderListSerializer,
    ProductSerializer,
    ProductImageSerializer,
    ProductOrderSerializer,
    ProductListSerializer, ProductRetrieveSerializer,
)


class DefaultSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "size"
    max_page_size = 100


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsAdminOrReadOnly,)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = DefaultSetPagination
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == "upload_image":
            serializer_class = ProductImageSerializer
        elif self.action == "list":
            serializer_class = ProductListSerializer
        elif self.action == "retrieve":
            serializer_class = ProductRetrieveSerializer
        return serializer_class

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

        if self.action == "retrieve":
            serializer = OrderRetrieveSerializer
        elif self.action == "list":
            serializer = OrderListSerializer
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
    pagination_class = DefaultSetPagination
    permission_classes = (IsAuthenticated,)
