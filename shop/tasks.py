# Create your tasks here

from shop.models import Product

from celery import shared_task


@shared_task
def count_products() -> int:
    return Product.objects.count()
