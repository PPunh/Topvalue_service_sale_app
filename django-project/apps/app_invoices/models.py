# coding=utf-8
from django.db import models, transaction
from django.db.models.signals import pre_save, post_save
from django.db.models import Sum
from django.dispatch import receiver
from decimal import Decimal
from datetime import date
# Forms and Models
from apps.app_customers.models import CustomersModel
from apps.app_employies.models import EmployiesModel

PREFIX = 'INV'

# Invoice Number Generator 
class InvoiceNumberGenerator(models.Model):
    invoice_runing_number = models.PositiveBigIntegerField(default=0)

    class Meta:
        verbose_name = 'ສ້າງເລກໃບເກັບເງິນອັດຕະໂນມັດ'
        verbose_name_plural = 'ສ້າງເລກໃບເກັບເງິນອັດຕະໂນມັດ'

    def __str__(self):
        return f"{self.invoice_runing_number}"


# Invoice Information Model 
class InvoiceInformationModel(models.Model):
    class INVOICE_STATUS(models.TextChoices):
        SENDED = 'sended', 'ສົ່ງໃບເກັບເງິນແລ້ວ'
        PAID = 'paid', 'ຈ່າຍແລ້ວ'
        PENDING = 'pending', 'ລໍຖ້າການຈ່າຍເງິນ'
        CANCELLED = 'cancelled', 'ຍົກເລີກ'

    invoice_number = models.CharField(max_length=20, primary_key=True)
    customer = models.ForeignKey(
        CustomersModel,
        on_delete=models.CASCADE,
        related_name='invoice_customer_information'
    )
    created_date = models.DateField()
    expired_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=INVOICE_STATUS.choices,
        default=INVOICE_STATUS.SENDED
    )
    create_by = models.ForeignKey(
        EmployiesModel,
        on_delete=models.SET_NULL,
        related_name='create_invoice_by',
        null=True,
        blank=True,
        default=None
    )
    total_all_products = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        editable=False,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'ຂໍ້ມູນໃບເກັບເງິນ'
        verbose_name_plural = 'ຂໍ້ມູນໃບເກັບເງິນ'

    def __str__(self):
        return f"ໃບສະເຫນີລາຄາເລກທີ່:{self.invoice_number} - ລູກຄ້າ: {self.customer.contact_person_name} - ວັນທີ່ອອກ: {self.created_date} - ບໍລິສັດ: {self.customer.company_name}"

    def calculate_total_all_product(self):
        total_sum = self.items.aggregate(total=Sum('total_one_product'))['total']
        if total_sum is None:
            total_sum = Decimal('0.00')
        if self.total_all_products != total_sum:
            self.total_all_products = total_sum
            self.save(update_fields=['total_all_products'])


# Invoice Items Model
class InvoiceItemsModel(models.Model):
    invoice = models.ForeignKey(
        InvoiceInformationModel,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product_name = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.IntegerField()
    period = models.IntegerField(default=12)
    total_one_product = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'ລາຍການສິນຄ້າ'
        verbose_name_plural = 'ລາຍການສິນຄ່າ'

    def __str__(self):
        return f"{self.product_name} - {self.price} x {self.qty} x {self.period}"

    def save(self, *args, **kwargs):
        if self.price and self.qty and self.period:
            self.total_one_product = self.price * self.qty * self.period
        else:
            self.total_one_product = Decimal('0.00')
        super().save(*args, **kwargs)
        self.invoice.calculate_total_all_product()  # Ensure total is updated

    def delete(self, *args, **kwargs):
        invoice_obj = self.invoice
        super().delete(*args, **kwargs)
        invoice_obj.calculate_total_all_product()


# Additional Expenses Model
class AdditionalExpenses(models.Model):
    invoice = models.OneToOneField(
        InvoiceInformationModel,
        on_delete=models.CASCADE,
        related_name='additional_expenses'
    )
    total_all_products_ref = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        editable=False,
        blank=True,
        null=True
    )
    it_service_percent = models.DecimalField(
        max_digits=5,
        decimal_places=0,
        null=True,
        blank=True
    )
    vat_percent = models.DecimalField(
        max_digits=5,
        decimal_places=0,
        blank=True,
        null=True
    )
    exchange_rate = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True
    )
    it_service_output = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        editable=False
    )
    vat_output = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        editable=False
    )
    exchange_rate_output = models.DecimalField(
        max_digits=20,
        decimal_places=0,
        blank=True,
        null=True,
        editable=False
    )
    grandTotal = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True,
        editable=False
    )

    class Meta:
        verbose_name = 'ຄ່າໃຊ້ຈ່າຍເພີ່ມເຕີ່ມ'
        verbose_name_plural = 'ຄ່າໃຊ້ຈ່າຍເພີ່ມເຕີ່ມ'

    def __str__(self):
        return f"Additional Expenses for invoices {self.invoice.invoice_number if self.invoice else 'N/A'}"

    def save(self, *args, **kwargs):
        self.total_all_products_ref = self.invoice.total_all_products or Decimal('0.00')
        base_amount = self.total_all_products_ref

        self.it_service_output = (
            base_amount * (self.it_service_percent / Decimal('100.00'))
            if self.it_service_percent else Decimal('0.00')
        )

        base_vat = base_amount + self.it_service_output
        self.vat_output = (
            base_vat * (self.vat_percent / Decimal('100.00'))
            if self.vat_percent else Decimal('0.00')
        )

        base_exchange = base_amount + self.it_service_output + self.vat_output
        self.exchange_rate_output = (
            base_exchange * self.exchange_rate
            if self.exchange_rate else Decimal('0.00')
        )

        self.grandTotal = base_amount + self.it_service_output + self.vat_output
        super().save(*args, **kwargs)


# Signal: Update AdditionalExpenses when Invoice is saved
@receiver(post_save, sender=InvoiceInformationModel)
def update_additional_expenses_on_quotation_save(sender, instance, created, **kwargs):
    def _do_update():
        if created:
            additional_expenses_obj, _ = AdditionalExpenses.objects.get_or_create(invoice=instance)
            additional_expenses_obj.save()
        elif hasattr(instance, 'additional_expenses'):
            instance.additional_expenses.save()
    transaction.on_commit(_do_update)


# Signal: Generate invoice number automatically
@receiver(pre_save, sender=InvoiceInformationModel)
def invoice_number_generator(sender, instance, **kwargs):
    if instance._state.adding and not instance.invoice_number:
        current_year = date.today().year
        prefix = f"{PREFIX}{current_year}"
        with transaction.atomic():
            generator, _ = InvoiceNumberGenerator.objects.select_for_update().get_or_create(pk=1)
            generator.invoice_runing_number += 1
            generator.save()
            instance.invoice_number = f"{prefix}{generator.invoice_runing_number:05d}"

    # if instance._state.adding and not instance.invoice_number:
    #     with transaction.atomic():
    #         generator, _ = InvoiceNumberGenerator.objects.select_for_update().get_or_create(pk=1)
    #         generator.invoice_runing_number += 1
    #         generator.save()
    #         instance.invoice_number = f"{PREFIX}{generator.invoice_runing_number:07d}"
