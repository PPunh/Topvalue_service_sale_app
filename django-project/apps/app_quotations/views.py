# coding=utf-8
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.db import transaction

#Login Request and rate_limit
from django_ratelimit.decorators import ratelimit
from django.contrib.auth.decorators import login_required
from django.conf import settings
#PDF
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.contrib.staticfiles import finders
from django.forms import inlineformset_factory

#Query
from django.db.models import Q

#Model and form
from .forms import QuotationInformationModelForm, CustomersModelForm, QuotationItemsFormSet, AdditionalExpensesFormSet
from .models import QuotationInformationModel, QuotationItemsModel, AdditionalExpenses
from apps.app_customers.models import CustomersModel
from apps.app_employies.models import EmployiesModel

#Function Views Here
#====================================== Home page and list of all quotations ======================================
@login_required
@ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True)
def home(request):
    query = request.GET.get("q", "")
    all_quotations = QuotationInformationModel.objects.all().order_by('expired_date')
    if query:
        all_quotations = all_quotations.filter(
            Q(quotation_id__icontains = query) |
            Q(customer__company_name__icontains=query)
        )
    template = 'app_quotations/home.html'
    context = {
        'title':'ລາຍການໃບສະເຫນີລາຄາ',
        'all_quotations':all_quotations
    }
    return render(request, template, context)



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
                #1 Save Customer first
                customer = customer_form.save()

                #2 Set customer and quotation and save quotation
                quotation = form.save(commit=False)
                try:
                    employies = EmployiesModel.objects.get(user=request.user)
                    quotation.create_by = employies
                except EmployiesModel.DoesNotExist:
                    return redirect('app_quotations:create_quotation')
                quotation.customer = customer
                quotation.save()

                #3 Save Formset
                item_formset.instance = quotation
                item_formset.save()

                if additional_expenses_formset.has_changed() or hasattr(quotation, 'additional_expenses'):
                    additional_expenses_formset.instance = quotation
                    additional_expenses_formset.save()
                messages.success(request, 'ອອກໃບສະເຫນີລາຄາໃຫມ່ ສຳເລັດ')
                return redirect('app_quotations:quotation_details', quotation_id=quotation.quotation_id)
    context = {
        'title':'ອອກໃບສະເຫນີລາຄາໃຫມ່',
        'form': form,
        'customer_form': customer_form,
        'item_formset': item_formset,
        'additional_expenses_formset': additional_expenses_formset,
        'quotation_instance': quotation_instance, #for check while edit or create new
    }
    return render (request, 'app_quotations/create_quotation.html', context)


#====================================== Delete Quotations ======================================
@login_required
@ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True)
def delete_quotation(request, quotation_id):
    delete_one_quotation = get_object_or_404(QuotationInformationModel, quotation_id=quotation_id)
    if request.method == 'POST':
        delete_one_quotation.delete()
        messages.success(request, 'ລຶບໃບສະເຫນີລາຄາສຳເລັດ')
        return redirect('app_quotations:home')
    context = {
        'title':'ລຶບໃບສະເຫນີລາຄາ',
        'delete_one_quotation':delete_one_quotation
    }
    return render(request, 'app_quotations/components/delete_quotation.html', context)


#====================================== Quotations Details ======================================
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

#====================================== Quotations Generator PDF======================================
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
