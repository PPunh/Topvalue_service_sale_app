from django.apps import AppConfig


# make sure to update AppClassName and App name
class AppInvoicesSmallConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'apps.app_invoices'
    verbose_name = 'ຈັດການໃບບິນເກັບເງິນ'
    label = 'app_invoices'
