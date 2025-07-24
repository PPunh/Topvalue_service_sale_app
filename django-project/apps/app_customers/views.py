# coding=utf-8
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404

# Import Forms and Models
from .forms import CustomersModelForm
from .models import CustomersModel


@method_decorator(ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True), name='dispatch')
class HomeView(LoginRequiredMixin, ListView):
    login_url = 'users:login' #Set url for Login Request
    model = CustomersModel
    template_name = 'app_customers/home.html'
    context_object_name = 'customers'

    #Search / Filter Functionz
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                customer_id__icontains=search
            ) | queryset.filter(
                company_name__icontains=search
            )
        return queryset

    #Sender the Searched term to template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['title'] = 'ລາຍການລູກຄ້າທັ່ງຫມົດ'
        return context


@method_decorator(ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True), name='dispatch')
class CustomerDetailsView(LoginRequiredMixin, DetailView):
    login_url = 'users:login'
    model = CustomersModel
    template_name = 'app_customers/customer_details.html'
    context_object_name = 'customer'

    #Override get_object to fetch the customer by customer_id
    def get_object(self, queryset = None):
        customer_id = self.kwargs.get('customer_id')
        return get_object_or_404(CustomersModel, customer_id=customer_id)

    #Sender the Searched term to template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "ລາຍລະອຽດຂອງລູກຄ້າ"
        return context

@method_decorator(ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True), name='dispatch')
class CustomersDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'users:login'
    model = CustomersModel
    template_name = 'app_customers/delete.html'
    success_url = reverse_lazy('app_customers:home')

    def get_object(self, queryset = None):
        customer_id = self.kwargs.get('customer_id')
        return get_object_or_404(CustomersModel, customer_id=customer_id)

    def form_valid(self, form):
        messages.success(self.request, 'ລູກຄ້າຖືກລຶບແລ້ວ')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ລຶບລູກຄ້າ'
        return context
