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
#=====[ Local App Imports: Forms ]=====
from .forms import (
    QuotationInformationModelForm,
    CustomersModelForm,
    QuotationItemsFormSet,
    AdditionalExpensesFormSet
)

#=====[ Local App Imports: Models ]=====
from .models import QuotationInformationModel, QuotationItemsModel, AdditionalExpenses
from apps.app_customers.models import CustomersModel
from apps.app_employies.models import EmployiesModel
# from apps.users.mixins import RoleRequiredMixin


#Function Views Here
#====================================== Home page and list of all quotations ======================================
@method_decorator(ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True), name='dispatch')
class HomeView(LoginRequiredMixin, ListView):
    login_url = 'users:login'
    model = QuotationInformationModel
    template_name = 'app_quotations/home.html'
    context_object_name = 'all_quotations'

    #Search / Filter Function
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                quotation_id__icontains = search
            ) | queryset.filter(
                customer__company_name__icontains = search
            )
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['title'] = 'ລາຍການໃບສະເຫນີລາຄາ'
        return context



#====================================== Add Quotations ======================================
@login_required
@ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True)
def create_quotation_with_customer(request, quotation_id=None):
    quotation_instance = None
    customer_instance = None

    if quotation_id:
        quotation_instance = get_object_or_404(QuotationInformationModel, pk=quotation_id)
        if hasattr(quotation_instance, 'customer'):
            customer_instance = quotation_instance.customer

    #Main Form
    form = QuotationInformationModelForm(request.POST or None, instance=quotation_instance)
    customer_form = CustomersModelForm(request.POST or None, instance=customer_instance, prefix='customer_form')
    #Customer form for items and addtional Expenses
    item_formset = QuotationItemsFormSet(request.POST or None, instance=quotation_instance, prefix='items')
    additional_expenses_formset = AdditionalExpensesFormSet(request.POST or None, instance=quotation_instance, prefix='expenses')

    if request.method == 'POST':
        if form.is_valid() and customer_form.is_valid() and item_formset.is_valid() and additional_expenses_formset.is_valid():
            with transaction.atomic():
                cleaned_data = customer_form.cleaned_data
                company_name = cleaned_data.get('company_name')
                contact_person_name = cleaned_data.get('contact_person_name')
                phone_number = cleaned_data.get('phone_number')
                email = cleaned_data.get('email')
                #Check customer is already in database will be not saved
                customer = CustomersModel.objects.filter(
                    company_name = company_name,
                    contact_person_name = contact_person_name,
                    phone_number = phone_number,
                    email = email
                ).first()
                if not customer:
                    customer = customer_form.save()
                else:
                    messages.info(request, 'ມີຂໍ້ມູນລູກຄ້ານີ້ໃນລະບົບແລ້ວ')

                #2 Set customer and quotation and save quotation
                quotation = form.save(commit=False)
                if not quotation.create_by:
                    try:
                        employies = EmployiesModel.objects.get(user=request.user)
                        quotation.create_by = employies
                    except EmployiesModel.DoesNotExist:
                        messages.error(request, 'ບໍ່ພົບຂໍ້ມູນພະນັກງານ ກະລຸນາຕິດຕໍ່ຫາຜູ້ດູແລລະບົບ')
                        return redirect('app_quotations:home')

                quotation.customer = customer
                quotation.save()

                #3 Save Formset
                item_formset.instance = quotation
                item_formset.save()

                if additional_expenses_formset.has_changed() or hasattr(quotation, 'additional_expenses'):
                    additional_expenses_formset.instance = quotation
                    additional_expenses_formset.save()
                if quotation_instance:
                    messages.success(request, 'ແກ້ໄຂໃບສະເຫນີລາຄາ ແລະ ລູກຄ້າ ສຳເລັດ')
                else:
                    messages.success(request, 'ອອກໃບສະເຫນີລາຄາໃຫມ່ ສຳເລັດ')

                return redirect('app_quotations:quotation_details', quotation_id=quotation.quotation_id)
    context = {
        'title': 'ແກ້ໄຂໃບສະເຫນີລາຄາ' if quotation_instance else 'ອອກໃບສະເຫນີລາຄາໃຫມ່',
        'form': form,
        'customer_form': customer_form,
        'item_formset': item_formset,
        'additional_expenses_formset': additional_expenses_formset,
        'quotation_instance': quotation_instance, #for check while edit or create new
    }
    return render (request, 'app_quotations/create_quotation.html', context)


#====================================== Delete Quotations ======================================
@method_decorator(
    ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True),
    name = 'dispatch'
)
class DeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'users:login'
    model = QuotationInformationModel
    template_name = 'app_quotations/components/delete_quotation.html'
    success_url = reverse_lazy('app_quotations:home')
    slug_field = 'quotation_id'
    slug_url_kwarg = 'quotation_id'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, "ລຶບໃບສະເຫນີລາຄາສຳເລັດ")
        return super().delete(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ລຶບໃບສະເຫນີລາຄາ'
        context['delete_one_quotation'] = self.get_object()
        return context


#====================================== Quotations Details ======================================
# @method_decorator(
#     ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True),
#     name = 'dispatch'
# )
# class DetailView(LoginRequiredMixin, DetailView):
#     login_url = 'users:login'
#     model = QuotationInformationModel
#     template_name = 'app_quotations/quotation_details.html'
#     slug_field = 'quotation_id'
#     slug_url_kwars = 'quotation_id'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)


@login_required
@ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True)
def quotation_details(request, quotation_id):
    one_quotation = get_object_or_404(QuotationInformationModel, quotation_id=quotation_id)
    quotation_items = one_quotation.items.all()  # related_name='items'
    additional_expense = getattr(one_quotation, 'additional_expenses', None)  # related_name='additional_expenses'
    context = {
        'title': 'ລາຍລະອຽດຂອງໃບສະເຫນີລາຄາ',
        'one_quotation': one_quotation,
        'quotation_items': quotation_items,
        'additional_expense': additional_expense,
        'total_price': one_quotation.total_all_products or 0,
        'it_service_amount': additional_expense.it_sevice_output if additional_expense else 0,
        'vat_amount': additional_expense.vat_output if additional_expense else 0,
        'grand_total': additional_expense.grandTotal if additional_expense else one_quotation.total_all_products or 0,
    }
    return render(request, 'app_quotations/quotation_details.html', context)


#====================================== Quotations Generator ======================================
@login_required
@ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True)
def generate_quotation_form(request, quotation_id):
    generate_quotation_form = get_object_or_404(QuotationInformationModel.objects.prefetch_related('items', 'additional_expenses'), quotation_id=quotation_id)
    template = 'app_quotations/components/quotation_form.html'
    context = {
        'title': f'ໃບສະເຫນີລາຄາເລກທີ່{quotation_id}',
        'generate_quotation_form':generate_quotation_form,
        'employies':generate_quotation_form.create_by or None
    }
    return render (request, template, context)

#==================================== Quotations Generator PDF with Signature =================================
@login_required
@ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True)
def quotation_generator_pdf(request, quotation_id):
    quotation = get_object_or_404(QuotationInformationModel, quotation_id=quotation_id)
    html_string = render_to_string('app_quotations/components/quotation_pdf_generator.html', {
        'generate_quotation_form': quotation,
        'quotation_id': quotation.quotation_id,
        'employies': quotation.create_by if hasattr(quotation, 'create_by') else None
    })
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f"attachment; filename=quotation_{quotation_id}.pdf"
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)
    return response


#================================ Quotations Generator PDF without Signature =================================
@login_required
@ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True)
def quotation_generator_pdf_no_sig(request, quotation_id):
    quotation = get_object_or_404(QuotationInformationModel, quotation_id=quotation_id)
    html_string = render_to_string('app_quotations/components/quotation_pdf_generator_no_sig.html', {
        'generate_quotation_form': quotation,
        'quotation_id': quotation.quotation_id,
    })
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f"attachment; filename=quotation_{quotation_id}.pdf"
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)
    return response
