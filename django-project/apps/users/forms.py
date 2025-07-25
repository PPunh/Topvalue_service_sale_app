from django import forms
from django.forms import ModelForm
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .backends import MultiAuthBackend

from . import models
from .models import User

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
    
class CustomerUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'phone_number',
            'password1',
            'password2'
        ]
        labels = {
            'username': 'ລະຫັດຜູ້ໃຊ້',
            'email': 'ອີເມວ',
            'phone_number': 'ເບີໂທລະສັບ',
            'password1': 'ລະຫັດຜ່ານ',
            'password2': 'ຢືນຢັນລະຫັດຜ່ານ',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        css_class = 'form-control w3-input w3-border w3-round-large w3-margin-bottom'
        for field in self.fields.values():
            field.widget.attrs['class']= f"{field.widget.attrs.get('class', '')} {css_class}".strip