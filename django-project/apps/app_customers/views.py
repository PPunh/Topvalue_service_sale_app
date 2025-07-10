# coding=utf-8
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

#Login Request and rate_limit
from django_ratelimit.decorators import ratelimit
from django.contrib.auth.decorators import login_required
from django.conf import settings

#Model
from .models import CustomersModel


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


@login_required
@ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True)
def customer_details(request, customer_id):
    one_customer = get_object_or_404(CustomersModel, customer_id=customer_id)
    template = 'app_customers/customer_details.html'
    context = {
        'title':'ລາຍລະອຽດຂອງລູກຄ້າ',
        'one_customer':one_customer
    }
    return render(request, template, context)
