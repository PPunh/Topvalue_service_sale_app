# coding=utf-8
from django.contrib import admin
from apps.app_employies.models import EmployiesModel


@admin.register(EmployiesModel)
class EmployiesModelAdmin(admin.ModelAdmin):
    list_display = ['employies_name', 'employies_lastname', 'department', 'create_date']
    search_fields = ['employies_name', 'employies_lastname', 'department']
    ordering = ('employies_id',)
    readonly_fields =('employies_id',)