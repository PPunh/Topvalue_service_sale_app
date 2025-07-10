# coding=utf-8
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction

#Login Request and rate_limit
from django_ratelimit.decorators import ratelimit
from django.contrib.auth.decorators import login_required
from django.conf import settings
#Login Request and rate_limit
#Import forms and models
from .forms import EmployiesModelForm
from .models import EmployiesModel


#Function Views Here
#====================================== Home page and list of all employies ======================================
@login_required
@ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True)
def home(requset):
    all_employies = EmployiesModel.objects.all().order_by('create_date')
    context = {
        'title':'ຂໍ້ມູນພະນັກງານ',
        'all_employies':all_employies
    }
    return render (requset, 'app_employies/home.html', context)


#====================================== Home page and list of add employies ======================================
@login_required
@ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True)
def add(request):
    if request.method == 'POST':
        form = EmployiesModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'ສ້າງບັນຊີພະນັກງານໃຫມ່ສຳເລັດ')
            return redirect('app_employies:home')
        else:
            messages.error(request, 'ສ້າງບັນຊີພະນັກງານລົ້ມເຫລວ')
            print(f" add_employies form errors: {form.errors}")
    else:
        form = EmployiesModelForm()
    context = {
        'title':'ສ້າງບັນຊີພະນັກງານ',
        'form':form
    }
    return render(request, 'app_employies/add.html', context)