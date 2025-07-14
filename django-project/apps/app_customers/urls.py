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
    path('', views.HomeView.as_view(), name='home'),
    path('customer/<str:customer_id>/', views.CustomerDetailsView.as_view(), name='customer_details'),
    path('delete/<str:customer_id>/', views.CustomersDeleteView.as_view(), name='delete'),
]

# when user go to path /app_name/ it will show api root page (endpoints list)
urlpatterns += router.urls
