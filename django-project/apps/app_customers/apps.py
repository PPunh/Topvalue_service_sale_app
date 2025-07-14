from django.apps import AppConfig


# make sure to update AppClassName and App name
class AppCustomersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'apps.app_customers'
    verbose_name = 'ການຈັດການລູກຄ້າ'
    label = 'app_customers'
