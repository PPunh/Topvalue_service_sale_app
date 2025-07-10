import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache
from django_ratelimit.decorators import ratelimit
from django.conf import settings

from . import forms
from . import models
from .forms import CustomerUserForm


logger = logging.getLogger(__name__)

@method_decorator(never_cache, name='dispatch')
@method_decorator(ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True), name='dispatch')
class Login(LoginView):
    '''user login using class base view (CBV)'''

    form_class = AuthenticationForm
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        # Get the default context provided by LoginView
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'  # Add custom context
        context['theme_color'] = 'w3-theme-blue.css'
        return context

    # redirect to page when login successful
    def get_success_url(self):
        messages.success(self.request, "ເຂົ້າສູ່ລະບົບສຳເລັດ")
        return reverse_lazy('app_quotations:home')

    def form_invalid(self, form):
        messages.error(self.request, "ລະຫັດຜູ້ໄຊ້ / ອີເມວ / ເບີໂທ ຫຼື ລະຫັດຜ່ານ ບໍ່ຖືກຕ້ອງ")
        return super().form_invalid(form)  # Re-render the form with errors message


@never_cache
@require_http_methods(["GET", "POST"])
@ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True)
def logout_view(request):
    logout(request)
    messages.success(request, "ທ່ານຳໄດ້ອອກຈາກລະບົບສຳເລັດ")
    return redirect('users:login')

@login_required
@ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True)
def create_user(request):
    if request.method == 'POST':
        form = CustomerUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'ສ້າງຊື່ຜູ້ໃຊ້ແລະລະຫັດຜ່ານສຳເລັດ')
            return redirect('app_employies:add')
        else:
            messages.error(request, 'ສ້າງບັນຊີພະນັກງານລົ້ມເຫລວ')
            print(f"add user and password form error: {form.errors}")
    else:
        form = CustomerUserForm()
    template = 'create_user.html'
    context = {
        'title':'ສ້າງບັນຊິພະນັກງານ',
        'form':form
    }
    return render(request, template, context)


@login_required
@ratelimit(key='header:X-Forwarded-For', rate=settings.RATE_LIMIT, block=True)
def home(request):
    context = {
        'title': 'Home',
    }

    template = 'home.html'
    return render(request, template, context)
