# Generated by Django 5.2.4 on 2025-07-07 08:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_quotations', '0005_remove_quotationsmodel_group_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quotationsmodel',
            name='period',
        ),
        migrations.RemoveField(
            model_name='quotationsmodel',
            name='price',
        ),
        migrations.RemoveField(
            model_name='quotationsmodel',
            name='product_name',
        ),
        migrations.RemoveField(
            model_name='quotationsmodel',
            name='qty',
        ),
        migrations.RemoveField(
            model_name='quotationsmodel',
            name='total_one_product',
        ),
        migrations.CreateModel(
            name='QuotationItemsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=60)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('qty', models.PositiveIntegerField()),
                ('period', models.IntegerField(default=12)),
                ('total_one_product', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10)),
                ('quotation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotation_items', to='app_quotations.quotationsmodel')),
            ],
            options={
                'verbose_name': 'Quotation Item',
                'verbose_name_plural': 'Quotation Items',
                'ordering': ['id'],
            },
        ),
    ]
