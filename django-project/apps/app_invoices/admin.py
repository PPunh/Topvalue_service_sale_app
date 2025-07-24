# coding=utf-8
from django.contrib import admin
from .models import InvoiceNumberGenerator, InvoiceInformationModel, InvoiceItemsModel, AdditionalExpenses

@admin.register(InvoiceNumberGenerator)
class InvoiceNumberGeneratorModelAdmin(admin.ModelAdmin):
    list_display = ('invoice_runing_number',)
    search_fields = ('invoice_runing_number',)

class InvoiceItemsInline(admin.TabularInline):
    model = InvoiceItemsModel
    extra = 1
    fields = ('product_name', 'price', 'qty', 'period', 'total_one_product')
    readonly_fields = ('total_one_product',)

class AdditionalExpensesInline(admin.StackedInline):
    model = AdditionalExpenses
    can_delete = False
    max_num = 1
    fields = (
        'total_all_products_ref',
        ('it_service_percent', 'it_service_output'),
        ('vat_percent', 'vat_output'),
        ('exchange_rate', 'exchange_rate_output'),
        'grandTotal'
    )
    readonly_fields = (
        'total_all_products_ref',
        'it_service_output',
        'vat_output',
        'exchange_rate_output',
        'grandTotal'
    )
@admin.register(InvoiceInformationModel)
class InvoiceInformationModelAdmin(admin.ModelAdmin):
    list_display = (
        'invoice_number',
        'customer',
        'created_date',
        'expired_date',
        'status',
        'total_all_products',
    )
    list_filter = ('status', 'created_date', 'expired_date')
    search_fields = (
        'invoice)number', 
        'customer__company_name',
        'customer__contact_person_name',
        'status'
    )
    date_hierarchy = 'created_date'
    inlines = [InvoiceItemsInline, AdditionalExpensesInline]
    readonly_fields = (
        'invoice_number',
        'total_all_products',
    )
    fieldsets = (
        ('ຂໍ້ມູນໃບສະເຫນີລາຄາ', {
            'fields': ('invoice_number', 'created_date', 'expired_date', 'status', 'total_all_products'),
        }),
        ('ຂໍ້ມູນລູກຄ້າ', {
            'fields': ('customer',),
        }),
    )