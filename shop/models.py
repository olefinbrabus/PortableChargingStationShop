import pathlib
from uuid import uuid4

from django.db import models
from django.db.models import indexes, UniqueConstraint
from django.utils.text import slugify

from user.models import User


def product_image_path(instance: "Product", filename: str) -> pathlib.Path:
    filename = f"{slugify(instance.name)}-{uuid4()}" + pathlib.Path(filename).suffix
    return pathlib.Path("upload/products/") / pathlib.Path(filename)


class Company(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    type_product = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    capacity = models.IntegerField()
    output = models.IntegerField()
    cycle_life = models.IntegerField()
    created_at = models.DateTimeField()
    image = models.ImageField(upload_to=product_image_path, null=True)

    class Meta:
        ordering = ('name',)
        constraints = [UniqueConstraint(
            fields=('name', 'type_product'),
            name='unique_product_name_type'
        )]

    def __str__(self):
        return f"{self.company.name} {self.name}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def subtotal(self):
        order_products = ProductOrder.objects.filter(order=self)
        price = 0
        if order_products.exists():
            for order_product in order_products:
                price += order_product.price
        return price

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.created_at} {self.user.email}"


class ProductOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
    ):
        self.price = self.product.price
        return super(ProductOrder, self).save(
            force_insert,
            force_update,
            using,
            update_fields
        )

    def __str__(self):
        return f"{self.product.name} в {self.order.id}"
