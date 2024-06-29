# Generated by Django 5.0.6 on 2024-06-27 07:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_productorder_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productorder',
            options={'default_related_name': 'product_orders'},
        ),
        migrations.AlterField(
            model_name='productorder',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.order'),
        ),
        migrations.AlterField(
            model_name='productorder',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product'),
        ),
    ]
