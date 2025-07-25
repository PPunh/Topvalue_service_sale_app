# coding=utf-8
# django libs
from django.urls import path, include

# 3rd party libs
from rest_framework.routers import DefaultRouter

# custom import
from . import views

# Namespace for URLs in this users app
app_name = 'app_invoices'
router = DefaultRouter()
# router.register('', views.ViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('HomeView/',views.HomeView.as_view(), name='home'),
    path('add/', views.create_invoice_with_customer, name='add'),
    path('Delete/<str:invoice_number>/delete', views.Delete.as_view(), name='delete'),
    path('Details/<str:invoice_number>/', views.Details.as_view(), name='details'),
    path('details/edit/<str:invoice_number>/',  views.create_invoice_with_customer, name='edit'),
    path('details/invoice_form/<str:invoice_number>', views.GenerateInvoiceFormView.as_view(), name='generate_invoice_form'),
    path('details/invoice_form/invoice_generate_pdf/<str:invoice_number>/', views.invoice_generate_pdf, name='invoice_generate_pdf'),
    path('details/invoice_form/invoice_generate_pdf_without_sig/<str:invoice_number>/', views.invoice_generate_pdf_without_sig, name='invoice_generate_pdf_without_sig'),
]

# when user go to path /app_name/ it will show api root page (endpoints list)
urlpatterns += router.urls
