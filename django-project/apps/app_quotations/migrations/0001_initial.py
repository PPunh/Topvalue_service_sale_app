# Generated by Django 5.2.3 on 2025-07-01 07:58

import django.db.models.deletion
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuotationNumberGenerator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quotation_running_number', models.PositiveBigIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='QuotationsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quotation_number', models.CharField(blank=True, max_length=20, unique=True)),
                ('product_name', models.CharField(max_length=60)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('qty', models.PositiveIntegerField()),
                ('period', models.IntegerField(default=12)),
                ('total_one_product', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10)),
                ('status', models.CharField(choices=[('ສັ່ງໃບເສະເຫນີລາຄາ', 'ສັ່ງ\u0e83ັບເສະເຫນີລາຄາ'), ('ປິດການຂາย', 'ປິດກາนຂາย'), ('ປະຕິເສິດກາนຂາย', 'ປະຕິເສິດກາนຂາย')], default='ສັ່ງ\u0e83ັບເສະເຫນີລາຄາ', max_length=30)),
                ('create_at', models.DateField()),
                ('expired_at', models.DateField()),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quotation_customer', to='app_customers.customersmodel')),
            ],
            options={
                'verbose_name': 'QuotationsModel',
                'verbose_name_plural': 'QuotationsModel',
                'ordering': ['quotation_number'],
            },
        ),
        migrations.CreateModel(
            name='AdditionalExpensesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('it_service_percent', models.DecimalField(blank=True, decimal_places=0, default=Decimal('0'), max_digits=5)),
                ('vat_percent', models.DecimalField(blank=True, decimal_places=0, default=Decimal('0'), max_digits=5)),
                ('exchange_rate', models.DecimalField(blank=True, decimal_places=2, default=Decimal('1'), max_digits=10)),
                ('it_service', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('vat', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('sum_all_products', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0.00'), max_digits=20)),
                ('rate_usd', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0.00'), max_digits=20)),
                ('grand_total_sum_all', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('quotation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='additional_expense', to='app_quotations.quotationsmodel')),
            ],
            options={
                'verbose_name': 'additional_expenses',
                'verbose_name_plural': 'additional_expenses',
            },
        ),
    ]
