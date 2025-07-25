# Generated by Django 5.2.4 on 2025-07-25 03:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_customers', '0002_alter_customersmodel_options'),
        ('app_quotations', '0010_quotationinformationmodel_create_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotationinformationmodel',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_information', to='app_customers.customersmodel'),
        ),
    ]
