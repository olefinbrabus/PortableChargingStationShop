# Generated by Django 5.0.6 on 2024-06-27 07:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_company_options_alter_productorder_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productorder',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_orders', to='shop.order'),
        ),
    ]