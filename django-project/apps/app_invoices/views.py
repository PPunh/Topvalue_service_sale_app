# coding=utf-8

#=====[ Built-in / Standard Library ]=====
import re
import tempfile
#=====[ Django Core Imports ]=====
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.staticfiles import finders
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
#=====[ Third-party Packages ]=====
from django_ratelimit.decorators import ratelimit
from weasyprint import HTML
#=====[ Django Forms & Formsets ]=====
from django.forms import inlineformset_factory

#Models and Forms
from .models import InvoiceInformationModel, InvoiceItemsModel, AdditionalExpenses
from apps.app_customers.models import CustomersModel
from apps.app_employies.models import EmployiesModel

from .forms import InvoiceInformationModelForm, CustomerModelForm, InvoiceItemsModelFormSet, AdditionalExpensesFormSet
#Function Views Here
#====================================== Home page and list of all quotations ======================================
@method_decorator(ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True), name='dispatch')
class HomeView(LoginRequiredMixin, ListView):
    login_url = 'users:login'
    model = InvoiceInformationModel
    template_name = 'app_invoices/home.html'
    context_object_name = 'all_invoices'

    # Search 
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                invoice_number__icontains = search
            ) | queryset.filter(
                customer__company_name__icontains = search
            )
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['title'] = 'ລາຍການໃບເກັບເງິນ'
        return context
    

@login_required
@ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True)
def create_invoice_with_customer(request, invoice_number=None):
    invoice_instance = None
    customer_instance = None

    if invoice_number:
        invoice_instance = get_object_or_404(InvoiceInformationModel, pk=invoice_number)
        if hasattr(invoice_instance, 'customer'):
            customer_instance = invoice_instance.customer

    # Main form 
    form = InvoiceInformationModelForm(request.POST or None, instance=invoice_instance)
    customer_form = CustomerModelForm(request.POST or None, instance=customer_instance, prefix='customer_form')
    item_formset = InvoiceItemsModelFormSet(request.POST or None, instance=invoice_instance, prefix='items')
    additional_expenses_formset = AdditionalExpensesFormSet(request.POST or None, instance=invoice_instance, prefix='expenses')

    if request.method == 'POST':
        if form.is_valid() and customer_form.is_valid() and item_formset.is_valid() and additional_expenses_formset.is_valid():
            with transaction.atomic():
                customer = customer_form.save()
                invoice = form.save(commit=False)
                if not invoice.create_by:
                    try:
                        employies = EmployiesModel.objects.get(user=request.user)
                        invoice.create_by = employies
                    except EmployiesModel.DoesNotExist:
                        pass
                invoice.customer = customer
                invoice.save()

                item_formset.instance = invoice
                item_formset.save()

                if additional_expenses_formset.has_changed() or hasattr(invoice, 'additional_expenses'):
                    additional_expenses_formset.instance = invoice
                    additional_expenses_formset.save()
                if invoice_instance:
                    messages.success(request, 'ແກ້ໄຂໃບເກັບເງິນສຳເລັດ')
                else:
                    messages.success(request, 'ອອກໃບເກັບເງິນສຳເລັດ')
                return redirect('app_invoices:details', invoice_number=invoice.invoice_number)
                # return redirect('app_invoices:home')
    context = {
        'title': 'ແກ້ໄຂໃບເກັບເງິນ' if invoice_instance else 'ອອກໃບເກັບເງິນໃຫມ່',
        'form': form,
        'customer_form': customer_form,
        'item_formset': item_formset,
        'additional_expenses_formset': additional_expenses_formset,
        'invoice_instance': invoice_instance,
    }
    return render (request, 'app_invoices/add.html', context)


# Delete 
@login_required
@ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True)
def delete(request, invoice_number):
    delete_one_invoice = get_object_or_404(InvoiceInformationModel, invoice_number=invoice_number)
    if request.method == 'POST':
        delete_one_invoice.delete()
        messages.success(request, 'ລຶບລາຍການໃບເກັບເງິນສຳເລັດ')
        return redirect('app_invoices:home')
    context = {
        'title':'ລຶບລາຍການໃບເກັບເງິນ',
        'delete_one_invoice':delete_one_invoice
    }
    return render (request, 'app_invoices/delete.html', context)

# Details 
@login_required
@ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True)
def details(request, invoice_number):
    one_invoice = get_object_or_404(InvoiceInformationModel, invoice_number=invoice_number)

    invoice_items = one_invoice.items.all()  # related_name='items'
    additional_expense = getattr(one_invoice, 'additional_expenses', None)  # related_name='additional_expenses'

    context = {
        'title': 'ລາຍລະອຽດຂອງໃບເກັບເງິນ',
        'one_invoice': one_invoice,
        'invoice_items': invoice_items,
        'additional_expense': additional_expense,
        'total_price': one_invoice.total_all_products or 0,
        'it_service_amount': additional_expense.it_service_output if additional_expense else 0,
        'vat_amount': additional_expense.vat_output if additional_expense else 0,
        'grand_total': additional_expense.grandTotal if additional_expense else one_invoice.total_all_products or 0,
    }

    return render(request, 'app_invoices/details.html', context)

#generate form
@login_required
@ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True)
def generate_invoice_form(request, invoice_number):
    generate_invoice_form = get_object_or_404(InvoiceInformationModel.objects.prefetch_related('items', 'additional_expenses'), invoice_number=invoice_number)
    template = 'app_invoices/components/invoice_form.html'
    context = {
        'title': f'ໃບເກັບເງິນເລກທີ່ {invoice_number}',
        'generate_invoice_form':generate_invoice_form,
        'employies':generate_invoice_form.create_by or None
    }
    return render (request, template, context)