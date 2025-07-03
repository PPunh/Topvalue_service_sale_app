# coding=utf-8
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

#Login Request and rate_limit
from django_ratelimit.decorators import ratelimit
from django.contrib.auth.decorators import login_required
from django.conf import settings

#Model
from .models import CustomersModel

#Form
from .forms import CustomersModelForm

#Function Views Here
#Home Page of App Customers
@login_required
@ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True)
def home(request):
    customers = CustomersModel.objects.all().order_by('-create_at')
    context = {
        'title': 'Home',
        'customers':customers
    }
    template = 'app_customers/home.html'
    return render(request, template, context)

#Add Customers of App Customers
@login_required
@ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True)
def add_customer (request):
    if request.method == 'POST':
        add_customer_form = CustomersModelForm(request.POST)
        if add_customer_form.is_valid():
            add_customer_form.save()
            messages.success(request, 'ສ້າງໃບສະເຫນີລາຄາໃຫມ່ ສຳເລັດ')
            return redirect('app_customers:home')
        else:
            messages.error(request, 'ສ້າງໃບສະເຫນີລາຄາບໍ່ສຳເລັດ')
            print(f"add_customers_form {add_customer_form.errors}")
    else:
        add_customer_form = CustomersModelForm()
    template = 'app_customers/add_customer.html'
    context = {
        'title': 'ສ້າງລາຍການລູກຄ້າໃຫມ່',
        'add_customer_form':add_customer_form
    }
    return render (request, template, context)