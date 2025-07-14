from django.apps import AppConfig


# make sure to update AppClassName and App name
class AppEmployiesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'apps.app_employies'
    verbose_name = 'ຈັດການພະນັກງານ'
    label = 'app_employies'
