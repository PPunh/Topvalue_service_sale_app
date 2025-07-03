# coding=utf-8
from django.contrib import admin
from django.utils import timezone
#from django.contrib.auth.admin import UserAdmin

from . import models
from . import forms


class ProfileAdmin(admin.ModelAdmin):
    model = models.Profile


class ProfileInline(admin.StackedInline):  # Or admin.TabularInline for a more compact view
    model = models.Profile
    can_delete = False  # Prevent deleting the profile directly from the user admin


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    model = models.User
    inlines = (ProfileInline,)

    def display_modified(self, obj): # display modified in local time
        return timezone.localtime(obj.date_modified).strftime('%Y-%m-%d %H:%M')

    display_modified.short_description = "Modified" #Set the column header

    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number',
                    'display_modified','modified_by')


admin.site.register(models.Profile)

'''
# method 1

@admin.register(ModelName)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ['field1', 'field2',]

# method 2

admin.site.register(models.User)
'''
