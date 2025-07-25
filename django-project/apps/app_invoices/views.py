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
from django.views.generic import ListView, DetailView, UpdateView,CreateView, FormView, TemplateView, DeleteView
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


# Create and Update Invoice
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
                cleaned_data = customer_form.cleaned_data
                company_name = cleaned_data.get('company_name')
                contact_person_name = cleaned_data.get('contact_person_name')
                phone_number = cleaned_data.get('phone_number')
                email = cleaned_data.get('email')

                # Check customer is aready in database will be not save
                customer = CustomersModel.objects.filter(
                    company_name=company_name,
                    contact_person_name=contact_person_name,
                    phone_number=phone_number,
                    email=email
                ).first()

                if not customer:
                    customer = customer_form.save()
                else:
                    messages.info(request, 'ມີຂໍ້ມູນລູກຄ້ານີ້ໃນລະບົບແລ້ວ')
                # Create Invoice
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

    context = {
        'title': 'ແກ້ໄຂໃບເກັບເງິນ' if invoice_instance else 'ອອກໃບເກັບເງິນໃຫມ່',
        'form': form,
        'customer_form': customer_form,
        'item_formset': item_formset,
        'additional_expenses_formset': additional_expenses_formset,
        'invoice_instance': invoice_instance,
    }
    return render(request, 'app_invoices/add.html', context)


# Delete
@method_decorator(
    ratelimit(key='header:X-Forwarded', rate=settings.RATE_LIMIT, block=True),
    name = 'dispatch'
)
class Delete(LoginRequiredMixin, DeleteView):
    login_url = 'users:login'
    template_name = 'app_invoices/delete.html'
    model = InvoiceInformationModel
    slug_field = 'invoice_number'
    slug_url_kwarg = 'invoice_number'
    success_url = reverse_lazy('app_invoices:home')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, 'ລຶບລາຍການໃບເກັບເງິນສຳເລັດ')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ລຶບລາຍການໃບເກັບເງິນ'
        context['delete_one_invoice'] = self.get_object()
        return context

# Details
@method_decorator(
    ratelimit(key='header:X-Forwarded', rate=settings.RATE_LIMIT, block=True),
    name = 'dispatch'
)
class Details(LoginRequiredMixin, DetailView):
    login_url = 'users:login'
    model = InvoiceInformationModel
    template_name = 'app_invoices/details.html'

    slug_field = 'invoice_number'
    slug_url_kwarg = 'invoice_number'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice = self.get_object()
        additional_expense = getattr(invoice, 'additional_expenses', None)
        context.update({
            'title': 'ລາຍລະອຽດຂອງໃບເກັບເງິນ',
            'one_invoice': invoice,
            'invoice_items': invoice.items.all(),
            'additional_expense': additional_expense,
            'total_price': invoice.total_all_products or 0,
            'it_service_amount': additional_expense.it_service_output if additional_expense else 0,
            'vat_amount': additional_expense.vat_output if additional_expense else 0,
            'grand_total': additional_expense.grandTotal if additional_expense else invoice.total_all_products or 0,
        })
        return context

#generate form
@method_decorator(
    ratelimit(key='header:X-Forwarded', rate=settings.RATE_LIMIT, block=True),
    name = 'dispatch'
)
class GenerateInvoiceFormView(LoginRequiredMixin, DetailView):
    login_url = 'users:login'
    model = InvoiceInformationModel
    template_name = 'app_invoices/components/invoice_form.html'
    slug_field = 'invoice_number'
    slug_url_kwarg = 'invoice_number'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('items', 'additional_expenses')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice = self.get_object()
        context['title'] = f"ໃບເກັບເງິນເລກທີ {invoice.invoice_number}"
        context['generate_invoice_form'] = invoice
        context['employies'] = invoice.create_by or None
        return context

# Generate PDF witSignature
@login_required
@ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True)
def invoice_generate_pdf(request, invoice_number):
    invoice = get_object_or_404(InvoiceInformationModel, invoice_number = invoice_number)
    html_string = render_to_string('app_invoices/components/invoice_generate_pdf_with_sig.html', {
        'invoice':invoice,
        'invoice_number':invoice.invoice_number,
        'employies':invoice.create_by or none
    })
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = f"attachment; filename=invoice_{invoice_number}.pdf"
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)
    return response

# Generate PDF without Signature
@login_required
@ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True)
def invoice_generate_pdf_without_sig(request, invoice_number):
    invoice = get_object_or_404(InvoiceInformationModel, invoice_number=invoice_number)
    html_string = render_to_string(
        'app_invoices/components/invoice_generate_pdf_without_sig.html',{
            'invoice':invoice,
            'invoice_number':invoice.invoice_number,
        }
    )
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f"attachment; filename=invoice_{invoice_number}.pdf"
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)
    return response
