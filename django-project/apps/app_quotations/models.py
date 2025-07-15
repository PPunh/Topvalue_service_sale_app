from django.db import models, transaction
from django.db.models.signals import pre_save, post_save
from django.db.models import Sum
from django.dispatch import receiver
from decimal import Decimal


#====================================== Import Models ======================================
from apps.app_customers.models import CustomersModel
from apps.app_employies.models import EmployiesModel
#====================================== Quotations PREFIX ======================================
PREFIX = 'QUO'

#====================================== Quotation_Runing_number ======================================
class QuotationIdGeneratorModel(models.Model):
    quotation_id_runing_number = models.PositiveBigIntegerField(default=0)

    class Meta:
        verbose_name = 'ສ້າງເລກໃບສະເຫນີລາຄາອັດຕະໂນມັດ'
        verbose_name_plural = 'ສ້າງເລກໃບສະເຫນີລາຄາອັດຕະໂນມັດ'
    def __str__(self):
        return f"{self.quotation_id_runing_number}"

#====================================== Quotation Information Model ======================================
class QuotationInformationModel(models.Model):
    # Recommended: Use TextChoices for better readability and safety
    class QuotationStatus(models.TextChoices):
        SENDED = 'sended', 'ສົ່ງໃບສະເຫນີລາຄາ'
        CLOSED = 'closed', 'ປິດການຂາຍ'
        CANCELLED = 'cancelled', 'ຍົກເລີກການຂາຍ'

    quotation_id = models.CharField(max_length=20, primary_key=True)
    customer = models.OneToOneField(CustomersModel, on_delete=models.CASCADE, related_name='customer_information')
    create_date = models.DateField()
    expired_date = models.DateField()
    # Use QuotationStatus.choices and QuotationStatus.SENDED
    status = models.CharField(max_length=20, choices=QuotationStatus.choices, default=QuotationStatus.SENDED)
    create_by = models.ForeignKey('app_employies.EmployiesModel', on_delete=models.SET_NULL, related_name='quotation', null=True, blank=True, default=None)
    total_all_products = models.DecimalField(max_digits=20, decimal_places=2, editable=False, blank=True, null=True)

    class Meta:
        verbose_name = 'ຂໍ້ມູນໃບສະເຫນີລາຄາ'
        verbose_name_plural = 'ຂໍ້ມູນໃບສະເຫນີລາຄາ'
        ordering = ('-expired_date',)

    def __str__(self):
        # Good for admin, maybe make it more user-friendly for general display
        return f"ໃບສະເຫນີລາຄາເລກທີ່:{self.quotation_id} - ລູກຄ້າ: {self.customer.company_name} - ວັນທີ່ອອກ: {self.create_date} - ບໍລິສັດ: {self.customer.company_name}"

    #=========== Calculate and Update value of all sum ================
    def calculate_total_all_products(self):
        # Use aggregate to sum all total_one_product from related items
        total_sum = self.items.aggregate(total=Sum('total_one_product'))['total']

        if total_sum is None: # If no items exist, sum will be None
            total_sum = Decimal('0.00')

        # Only save if the value has changed to prevent unnecessary DB writes/signal triggers
        if self.total_all_products != total_sum:
            self.total_all_products = total_sum
            # Use update_fields to save only this specific field, good practice
            self.save(update_fields=['total_all_products'])

#====================================== Quotation Items Model ======================================
class QuotationItemsModel(models.Model):
    quotation = models.ForeignKey(QuotationInformationModel, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.IntegerField()
    period = models.IntegerField(default=12) #Months - Clarify unit (months/years) in comments if not obvious
    total_one_product = models.DecimalField(max_digits=10, decimal_places=2, editable=False, blank=True, null=True)

    class Meta:
        verbose_name ='ລາຍການສິນຄ້າ'
        verbose_name_plural = 'ລາຍການສິນຄ້າ'

    def __str__(self):
        # Make __str__ concise for admin display
        return f"{self.product_name} x {self.qty} @ {self.price}"

    #============ Calculate and save ===============
    def save(self, *args, **kwargs):
        if self.price is not None and self.qty is not None and self.period is not None:
            self.total_one_product = self.price * self.qty * self.period
        else:
            self.total_one_product = Decimal('0.00')

        super().save(*args, **kwargs) # Save the current QuotationItemsModel instance first

        # After saving the item, trigger the recalculation of the parent quotation's total
        self.quotation.calculate_total_all_products()

    #============ Delete Function ===============
    def delete(self, *args, **kwargs):
        # Before deleting QuotationItemModel, get a reference to the associated quotation
        # This is crucial because self.quotation will be None after super().delete()
        quotation_obj = self.quotation

        super().delete(*args, **kwargs) # Perform the actual deletion of the item

        # After deletion, trigger the recalculation on the parent quotation
        # Use the stored reference
        quotation_obj.calculate_total_all_products()

#====================================== Additional Expenses ======================================
class AdditionalExpenses(models.Model):
    quotation = models.OneToOneField(QuotationInformationModel, on_delete=models.CASCADE, related_name='additional_expenses') # Consistent related_name spelling

    # This field reflects the sum from QuotationInformationModel
    total_all_products_ref = models.DecimalField(
        max_digits=20, decimal_places=2, editable=False, blank=True, null=True
    )
    #=========== input value with percentage ================
    # Adjusted max_digits and decimal_places for percentages and exchange rates
    it_service_percent = models.DecimalField(max_digits=5, decimal_places=0, null=True, blank=True)
    vat_percent = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    #=========== output  ================
    it_sevice_output = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, editable=False)
    vat_output = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, editable=False)
    exchange_rate_output = models.DecimalField(max_digits=20, decimal_places=0, blank=True, null=True, editable=False)

    #=========== Grand Total ================
    grandTotal = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, editable=False)

    class Meta:
        verbose_name = 'ຄ່າໃຊ້ຈ່າຍເພີ່ມເຕີ່ມ'
        verbose_name_plural = 'ຄ່າໃຊ້ຈ່າຍເພີ່ມເຕີ່ມ'

    def __str__(self):
        return f"Additional Expenses for Quotation {self.quotation.quotation_id if self.quotation else 'N/A'}" # More robust __str__

    #=========== Recalculate ================
    def save(self, *args, **kwargs):
        # Get total_all_products from QuotationInformationModel (use the field, not the method)
        if self.quotation and self.quotation.total_all_products is not None:
            self.total_all_products_ref = self.quotation.total_all_products
        else:
            self.total_all_products_ref = Decimal('0.00')

        base_amount = self.total_all_products_ref

        #=========== IT_Service Output ================
        if self.it_service_percent is not None:
            # Ensure division by Decimal for precision
            self.it_sevice_output = base_amount * (self.it_service_percent / Decimal('100.00'))
        else:
            self.it_sevice_output = Decimal('0.00')

        #=========== Vat Output ================
        vat_base = base_amount + self.it_sevice_output #Sum base amount first and calculate vat
        if self.vat_percent is not None:
            self.vat_output = vat_base * (self.vat_percent / Decimal('100.00'))
        else:
            self.vat_output = Decimal('0.00')

        #=========== Exchange Rate Output ================
        base_exchange = base_amount + self.it_sevice_output + self.vat_output
        if self.exchange_rate is not None and self.exchange_rate != Decimal('0.00'):
            # Example calculation: if base_amount is in USD and you want to convert to LAK
            self.exchange_rate_output = base_exchange * self.exchange_rate
        else:
            self.exchange_rate_output = Decimal('0.00') # Corrected: use Decimal('0.00')

        #=========== Grand Total ================
        self.grandTotal = base_amount + self.it_sevice_output + self.vat_output
        # Add other outputs if they contribute to grand total, e.g. + self.exchange_rate_output (if applicable)

        super().save(*args, **kwargs)

#====================================== Signal for Update AdditionalExpenses when saved QuotationInformationModel ======================================
@receiver(post_save, sender=QuotationInformationModel)
def update_additional_expenses_on_quotation_save(sender, instance, created, **kwargs):
    def _do_update():
        if created:
            # AdditionalExpenses.objects.create(quotation=instance)
            additional_expenses_obj, _ = AdditionalExpenses.objects.get_or_create(quotation=instance)
            additional_expenses_obj.save()
        elif hasattr(instance, 'additional_expenses'):
            instance.additional_expenses.save()

    transaction.on_commit(_do_update)

#====================================== Generate Quotation Runing Number Function ======================================
@receiver(pre_save, sender=QuotationInformationModel)
def quotation_id_generator(sender, instance, **kwargs): # Changed render to sender for clarity
    # Only generate ID if it's a new instance and quotation_id is not already set
    if instance._state.adding and not instance.quotation_id:
        with transaction.atomic():
            # Use id=1 or a specific pk if you only have one generator instance
            generator, created = QuotationIdGeneratorModel.objects.select_for_update().get_or_create(pk=1)
            generator.quotation_id_runing_number += 1
            generator.save()
            instance.quotation_id = f"{PREFIX}{generator.quotation_id_runing_number:07d}"
