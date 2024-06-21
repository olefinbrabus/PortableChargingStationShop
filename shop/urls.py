from django.urls import path, include
from rest_framework import routers

from shop.views import CompanyViewSet, ProductViewSet, OrderViewSet


router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'products', ProductViewSet)
router.register('orders', OrderViewSet)

urlpatterns = [path('', include(router.urls))]
