# coding=utf-8
# django libs
from django.urls import path, include

# 3rd party libs
from rest_framework.routers import DefaultRouter

# custom import
from . import views

# Namespace for URLs in this users app
app_name = 'app_label'
router = DefaultRouter()
# router.register('', views.ViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('HomeView/',views.HomeView.as_view(), name='home'),
    path('add/', views.create_invoice_with_customer, name='add'),
    path('delete/<str:invoice_number>/delete', views.delete, name='delete'),
    path('details/<str:invoice_number>', views.details, name='details'),
    path('details/edit/<str:invoice_number>/',  views.create_invoice_with_customer, name='edit'),
    path('details/invoice_form/<str:invoice_number>/', views.generate_invoice_form, name='generate_invoice_form'),
]

# when user go to path /app_name/ it will show api root page (endpoints list)
urlpatterns += router.urls
