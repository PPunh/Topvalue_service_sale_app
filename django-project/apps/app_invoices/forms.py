# coding=utf-8
from django import forms
from django.forms import ModelForm

# from .models import *


'''
# model form snipet

class ModelNameForm(forms.ModelForm):

    class Meta:
        model = ModelName
        fields = ['x', 'y', 'z']

        labels = {
            'x': 'Name x',
            'y': 'Name y',
            'z': 'Name Z',
        }

    def __init__(self, *args, **kwargs):
        super(ModelNameForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ModelNameForm, self).clean()
        return cleaned_data
'''
