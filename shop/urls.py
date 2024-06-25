from django.urls import path, include
from rest_framework import routers

from shop.views import CompanyViewSet, ProductViewSet, OrderViewSet, ProductOrderViewSet


router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'product_orders', ProductOrderViewSet)

urlpatterns = [path('', include(router.urls))]
