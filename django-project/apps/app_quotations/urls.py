# coding=utf-8
# django libs
from django.urls import path, include

# 3rd party libs
from rest_framework.routers import DefaultRouter

# custom import
from . import views

# Namespace for URLs in this users app
app_name = 'app_quotations'
router = DefaultRouter()
# router.register('', views.ViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.HomeView.as_view(), name='home'),
    path('create_quotation/', views.create_quotation_with_customer, name='create_quotation'),
    path('delete_quotation/<str:quotation_id>/delete', views.delete_quotation, name='delete_quotation'),
    path('quotation_details/<str:quotation_id>/', views.quotation_details, name='quotation_details'),
    path('quotation_details/edit_quotation/<str:quotation_id>/', views.create_quotation_with_customer, name='edit_quotation'),
    path('quotation_details/quotation_form/<str:quotation_id>/', views.generate_quotation_form, name='generate_quotation_form'),
    path('quotation_details/quotation_form/quotation_pdf_generator/<str:quotation_id>/', views.quotation_generator_pdf, name='quotation_generator_pdf'),
    path('quotation_details/quotation_form/quotation_generator_pdf_no_sig/<str:quotation_id>/', views.quotation_generator_pdf_no_sig, name='quotation_generator_pdf_no_sig'),
]

# when user go to path /app_name/ it will show api root page (endpoints list)
urlpatterns += router.urls
