# coding=utf-8
from django.db import models
from django.utils import timezone
import uuid

##################### Import Model
from apps.users.models import User


class EmployiesModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    employies_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employies_name = models.CharField(max_length=30)
    employies_lastname = models.CharField(max_length=30)
    department = models.CharField(max_length=30)
    signature = models.ImageField(upload_to='employies_signatures')
    create_date = models.DateField(auto_now_add=timezone.now)

    class Meta:
        verbose_name = 'ຂໍ້ມູນພະນັກງານ'
        verbose_name_plural = 'ຂໍ້ມູນພະນັກງານ'
        ordering = ('employies_id',)

    def __str__(self):
        return f"{self.employies_id} - {self.employies_name} - {self.employies_lastname} - {self.department}"
    
    def delete(self, *args, **kwargs):
        user = self.user
        if user and user.pk is not None:
            user.delete()
        super().delete(*args, **kwargs)