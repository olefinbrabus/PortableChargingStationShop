from django.utils import timezone
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from shop.models import Product, Company, Order, ProductOrder
from shop.serializers import (
    ProductListSerializer,
    ProductRetrieveSerializer,
    OrderListSerializer,
)
from user.models import User

PRODUCTS_URL = reverse("shop:product-list")
COMPANIES_URL = reverse("shop:company-list")
ORDERS_URL = reverse("shop:order-list")


def sample_product(**kwargs) -> Product:
    company = Company.objects.create(
        name=kwargs.pop("name_company", f"Test Company{len(Company.objects.all()) + 1}")
    )

    defaults = {
        "name": "Test Product",
        "type_product": "test",
        "company": company,
        "price": 10.1,
        "capacity": 10,
        "output": 10,
        "cycle_life": 5,
        "created_at": timezone.now(),
    }
    defaults.update(kwargs)
    return Product.objects.create(**defaults)


def sample_order_product_order(user: User, *products_id):
    order = Order.objects.create(user=user)

    product_orders = [] * len(products_id)
    for product_id in products_id:
        product_order = ProductOrder.objects.create(
            product=Product.objects.get(pk=product_id.id),
            order=order,
        )
        product_orders.append(product_order)
    return order, product_orders


def detail_product_url(product_id: int):
    return reverse("shop:product-detail", kwargs={"pk": product_id})


class UnAuthenticationShopApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_not_required_in_products(self):
        response = self.client.get(PRODUCTS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_auth_not_required_in_companies(self):
        response = self.client.get(COMPANIES_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_auth_required_in_orders(self):
        response = self.client.get(ORDERS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_products(self):
        sample_product()

        response = self.client.get(PRODUCTS_URL)

        products = Product.objects.all()
        serializer = ProductListSerializer(products, many=True)
        self.assertEqual(response.data["results"], serializer.data)

    def test_filter_products(self):
        product_with_default_company = sample_product()
        product_with_custom_company = sample_product(
            name_company="Test2", name="TestCase"
        )

        response = self.client.get(
            PRODUCTS_URL, {"company": f"{product_with_custom_company.company.id}"}
        )
        serializer_default_company = ProductListSerializer(product_with_default_company)
        serializer_custom_company = ProductListSerializer(product_with_custom_company)

        self.assertNotIn(serializer_default_company.data, response.data["results"])
        self.assertIn(serializer_custom_company.data, response.data["results"])

    def test_retrieve_products(self):
        product = sample_product()

        product_url = detail_product_url(product.id)
        response = self.client.get(product_url)

        serializer = ProductRetrieveSerializer(product)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class AuthenticationShopApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@example.com",
            password="test_example123",
        )
        self.client.force_authenticate(user=self.user)

    def test_auth_required_in_orders(self):
        response = self.client.get(ORDERS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product_forbidden(self):
        company = Company.objects.create(name="Test Company")

        payload = {
            "name": "Bad Product",
            "type_product": "bad",
            "company": company,
            "price": 102.1,
            "capacity": 102,
            "output": 102,
            "cycle_life": -1,
            "created_at": timezone.now(),
        }

        response = self.client.post(PRODUCTS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_product_order_created_checked(self):
        product = sample_product()
        order, product_orders = sample_order_product_order(self.user, product)
        serializer = OrderListSerializer(order)
        serializer.product_orders = product_orders.pop()

        response = self.client.get(ORDERS_URL)
        self.assertEqual(response.data["results"], [serializer.data])


class AdminShopApiTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="test_example123",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_product(self):
        company = Company.objects.create(name="Test Company")

        payload = {
            "name": "Test Product",
            "type_product": "test123",
            "company": company.id,
            "price": 10.1,
            "capacity": 10,
            "output": 10,
            "cycle_life": 5,
            "created_at": timezone.now(),
        }

        response = self.client.post(PRODUCTS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
