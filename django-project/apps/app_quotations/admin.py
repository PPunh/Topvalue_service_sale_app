from django.contrib import admin
from .models import QuotationsModel, AdditionalExpensesModel, QuotationNumberGenerator


# Inline สำหรับ AdditionalExpensesModel (1:1 กับใบเสนอราคา)
class AdditionalExpensesInline(admin.StackedInline):
    model = AdditionalExpensesModel
    can_delete = False
    max_num = 1
    readonly_fields = (
        'it_service',
        'vat',
        'sum_all_products',
        'exchange_result',
        'grand_total_sum_all',
    )


@admin.register(QuotationsModel)
class QuotationsAdmin(admin.ModelAdmin):
    list_display = ('quotation_number', 'customer', 'product_name', 'qty', 'period', 'total_one_product', 'status', 'create_at', 'expired_at')
    search_fields = ('quotation_number', 'product_name', 'customer__name')
    list_filter = ('status', 'create_at')
    readonly_fields = ('quotation_number', 'total_one_product')
    inlines = [AdditionalExpensesInline]


@admin.register(QuotationNumberGenerator)
class QuotationNumberGeneratorAdmin(admin.ModelAdmin):
    list_display = ('id', 'quotation_running_number')
