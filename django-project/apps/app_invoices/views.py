# coding=utf-8
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404



# @method_decorator(ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True), name='dispatch')

def home(request):
    return render(request, 'app_invoices/home.html')