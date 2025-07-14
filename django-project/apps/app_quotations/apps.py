from django.apps import AppConfig


# make sure to update AppClassName and App name
class AppQuotationsSmallConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'apps.app_quotations'
    verbose_name = 'ການຈັດການໃບວະເຫນີລາຄາ'
    label = 'app_quotations'
