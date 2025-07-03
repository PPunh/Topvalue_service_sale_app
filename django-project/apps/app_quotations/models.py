from django.db import models
from django.utils.timezone import now
from decimal import Decimal
from django.db.models.signals import pre_save
from django.db import transaction
from django.dispatch import receiver

from apps.app_customers.models import CustomersModel

PREFIX = 'QUO'

# ---------- Quotation Model ----------
class QuotationsModel(models.Model):
    quotation_number = models.CharField(max_length=20, unique=True, blank=True)
    customer = models.ForeignKey(
        CustomersModel, on_delete=models.CASCADE,
        related_name='quotations',
        null=True
    )
    product_name = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.PositiveIntegerField()
    period = models.IntegerField(default=12)
    total_one_product = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    status = models.CharField(max_length=30, choices=[
        ('ສັ່ງໃບເສະເຫນີລາຄາ', 'ສັ່ງໃບເສະເຫນີລາຄາ'),
        ('ປິດການຂາຍ', 'ປິດການຂາຍ'),
        ('ປະຕິເສິດການຂາຍ', 'ປະຕິເສິດການຂາຍ'),
    ], default='ສັ່ງໃບເສະເຫນີລາຄາ')
    create_at = models.DateField(blank=True, null=True)
    expired_at = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Quotation'
        verbose_name_plural = 'Quotations'
        ordering = ['quotation_number']

    def __str__(self):
        return f"{self.quotation_number} | {self.product_name} | {self.status}"

    def save(self, *args, **kwargs):
        if not self.create_at:
            self.create_at = now().date()
        self.total_one_product = self.price * self.qty * self.period
        super().save(*args, **kwargs)


# ---------- Additional Expenses Model ----------
class AdditionalExpensesModel(models.Model):
    quotation = models.OneToOneField(
        QuotationsModel,
        on_delete=models.CASCADE,
        related_name='additional_expenses',
        null=True
    )
    it_service_percent = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    vat_percent = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    exchange_rate = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('1.00'))

    # Fields Auto Calculate
    it_service = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    vat = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    sum_all_products = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    exchange_result = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    grand_total_sum_all = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        verbose_name = 'Additional Expense'
        verbose_name_plural = 'Additional Expenses'

    def __str__(self):
        return f"Expenses for {self.quotation.quotation_number}"

    def calculate_totals(self):
        if self.quotation:
            total = self.quotation.total_one_product

            self.it_service = (self.it_service_percent / Decimal('100')) * total
            self.vat = (self.vat_percent / Decimal('100')) * (total + self.it_service)
            self.sum_all_products = total + self.it_service + self.vat
            self.exchange_result = self.sum_all_products * self.exchange_rate
            self.grand_total_sum_all = self.sum_all_products
        else:
            # ไม่คำนวณอะไรถ้าไม่มี quotation
            self.it_service = Decimal('0.00')
            self.vat = Decimal('0.00')
            self.sum_all_products = Decimal('0.00')
            self.exchange_result = Decimal('0.00')
            self.grand_total_sum_all = Decimal('0.00')


    def save(self, *args, **kwargs):
        self.calculate_totals()
        super().save(*args, **kwargs)


# ---------- Quotation Number Generator ----------
class QuotationNumberGenerator(models.Model):
    quotation_running_number = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f"Quotation Number Generator {self.quotation_running_number}"


# ---------- Signal generate quotation_number ----------
@receiver(pre_save, sender=QuotationsModel)
def quotation_number_generator(sender, instance, **kwargs):
    if instance._state.adding and not instance.quotation_number:
        with transaction.atomic():
            generator, _ = QuotationNumberGenerator.objects.select_for_update().get_or_create(id=1)
            generator.quotation_running_number += 1
            generator.save()
            instance.quotation_number = f"{PREFIX}{generator.quotation_running_number:05d}"
