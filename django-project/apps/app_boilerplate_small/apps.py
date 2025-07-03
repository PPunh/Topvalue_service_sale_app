from django.apps import AppConfig


# make sure to update AppClassName and App name
class AppBoilerplateSmallConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'apps.app_boilerplate_small'
    verbose_name = 'Application Boilerplate for Small App'
    label = 'name of the app'
