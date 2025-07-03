# coding=utf-8
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

#Login Request and rate_limit
from django_ratelimit.decorators import ratelimit
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db import transaction

#Model
from .models import QuotationsModel, AdditionalExpensesModel
from apps.app_customers.models import CustomersModel

#Form
from .forms import QuotationsModelForm, AdditionalExpensesModelForm, QuotationsModelFormSet
from apps.app_customers.forms import CustomersModelForm

#Function Views Here
#Home Page of App Customers
@login_required
@ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True)
def home(request):
    quotations = QuotationsModel.objects.select_related('customer').prefetch_related('additional_expenses')
    template = 'app_quotations/home.html'
    context = {
        'title':'ລາຍການໃບສະເຫນີລາຄາ',
        'quotations':quotations
    }
    return render(request, template, context)


@login_required
@ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True)
def create_quotation(request):
    if request.method == 'POST':
        customer_form = CustomersModelForm(request.POST)
        additional_form = AdditionalExpensesModelForm(request.POST)
        quotation_formset = QuotationsModelFormSet(request.POST, queryset=QuotationsModel.objects.none())

        if customer_form.is_valid() and additional_form.is_valid() and quotation_formset.is_valid():
            with transaction.atomic():
                # Save customer first
                customer = customer_form.save()

                # Save all quotation items
                quotations = quotation_formset.save(commit=False)
                for quotation in quotations:
                    quotation.customer = customer
                    quotation.save()

                # Save additional expense only if there is at least one quotation
                if quotations:
                    additional_expense = additional_form.save(commit=False)
                    additional_expense.quotation = quotations[0]  # Use the first quotation
                    additional_expense.calculate_totals()         # Ensure calculation before save
                    additional_expense.save()

            messages.success(request, "ສ້າງໃບເສະເຫນີລາຄາສຳເລັດ!")
            return redirect('app_quotations:home')
        else:
            messages.error(request, "ກວດສອບຂໍ້ມູນກ່ອນບັນທຶກ")
    else:
        customer_form = CustomersModelForm()
        additional_form = AdditionalExpensesModelForm()
        quotation_formset = QuotationsModelFormSet(queryset=QuotationsModel.objects.none())

    context = {
        'customer_form': customer_form,
        'additional_form': additional_form,
        'quotation_formset': quotation_formset,
    }
    return render(request, 'app_quotations/create_quotation.html', context)

