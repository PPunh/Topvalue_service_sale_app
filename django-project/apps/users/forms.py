from django import forms
from django.forms import ModelForm
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .backends import MultiAuthBackend

from . import models

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, label="Usename / Email / Phone number")
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if self.request:
            pass

    '''
    AxesBackendRequestParameterRequired at /login/ AxesBackend requires a request as an argument to authenticate
    but the built-in LoginView CBV not sending the request object to AxesBackend, need to modify the
    authenticate() method so that it include request object.
    '''
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = MultiAuthBackend().authenticate(request=self.request,username=username, password=password,
                                        backend='users.backends.MultiAuthBackend')  # Pass the request here
            if user is None:
                raise forms.ValidationError("Invalid username or password.")
            else:
                self.user_cache = user

        return self.cleaned_data
