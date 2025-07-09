from django.db import models, transaction
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Models
from apps.users.models import User

# PREFIX
PREFIX = 'CUS_ID'


class CustomersIdGenerator(models.Model):
    customer_running_number = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f"{self.customer_running_number}"


class CustomersModel(models.Model):
    customer_id = models.CharField(max_length=20, unique=True, blank=True)
    company_name = models.CharField(max_length=30)
    contact_person_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=8)
    email = models.EmailField(max_length=50)
    company_address = models.CharField(max_length=255)
    create_at = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = 'ຂໍ້ມູນກ່ຽວກັບລູກຄ້າ'
        verbose_name_plural = 'ຂໍ້ມູນກ່ຽວກັບລູກຄ້າ'
        ordering = ('-create_at',)

    def __str__(self):
        return f"{self.customer_id} - {self.company_name} - {self.contact_person_name} - {self.phone_number} - {self.email} - {self.create_at}"


@receiver(pre_save, sender=CustomersModel)
def customer_id_generator(sender, instance, **kwargs):
    if instance._state.adding and not instance.customer_id:
        with transaction.atomic():
            generator, created = CustomersIdGenerator.objects.select_for_update().get_or_create(id=1)
            generator.customer_running_number += 1
            generator.save()
            instance.customer_id = f"{PREFIX}{generator.customer_running_number:05d}"
