# coding=utf-8
# django libs
from django.urls import path, include

# 3rd party libs
from rest_framework.routers import DefaultRouter

# custom import
from . import views

# Namespace for URLs in this users app
app_name = 'app_customers'
router = DefaultRouter()
# router.register('', views.ViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.home, name='home'),
    path('customer_details/<str:customer_id>/', views.customer_details, name="customer_details"),
]

# when user go to path /app_name/ it will show api root page (endpoints list)
urlpatterns += router.urls
