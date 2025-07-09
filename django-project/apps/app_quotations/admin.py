from django.contrib import admin
from .models import (
    QuotationIdGeneratorModel,
    QuotationInformationModel,
    QuotationItemsModel,
    AdditionalExpenses
)

@admin.register(QuotationIdGeneratorModel)
class QuotationIdGeneratorModelAdmin(admin.ModelAdmin):
    list_display = ('quotation_id_runing_number',)
    search_fields = ('quotation_id_runing_number',)

class QuotationItemsInline(admin.TabularInline):
    model = QuotationItemsModel
    extra = 1
    fields = ('product_name', 'price', 'qty', 'period', 'total_one_product')
    readonly_fields = ('total_one_product',)

class AdditionalExpensesInline(admin.StackedInline):
    model = AdditionalExpenses
    can_delete = False
    max_num = 1
    fields = (
        'total_all_products_ref',
        ('it_service_percent', 'it_sevice_output'),
        ('vat_percent', 'vat_output'),
        ('exchange_rate', 'exchange_rate_output'),
        'grandTotal'
    )
    readonly_fields = (
        'total_all_products_ref',
        'it_sevice_output',
        'vat_output',
        'exchange_rate_output',
        'grandTotal'
    )

@admin.register(QuotationInformationModel)
class QuotationInformationModelAdmin(admin.ModelAdmin):
    list_display = (
        'quotation_id',
        'customer',
        'create_date',
        'expired_date',
        'status',
        'total_all_products',
    )
    list_filter = ('status', 'create_date', 'expired_date')
    search_fields = (
        'quotation_id', 
        'customer__company_name',
        'customer__contact_person_name',
        'status'
    )
    date_hierarchy = 'create_date' 
    inlines = [QuotationItemsInline, AdditionalExpensesInline]
    readonly_fields = (
        'quotation_id',
        'create_date',
        'total_all_products',
    )
    
    fieldsets = (
        ('ຂໍ້ມູນໃບສະເຫນີລາຄາ', {
            'fields': ('quotation_id', 'create_date', 'expired_date', 'status', 'total_all_products'),
        }),
        ('ຂໍ້ມູນລູກຄ້າ', {
            'fields': ('customer',),
        }),
    )
