# coding=utf-8
from django import forms
from .models import CustomersModel


class CustomersModelForm(forms.ModelForm):
    class Meta:
        model = CustomersModel
        fields = ['company_name', 'contact_person_name', 'phone_number', 'email', 'company_address']
        labels = {
            'company_name': 'ບໍລິສັດ',
            'contact_person_name': 'ຜູ້ຕິດຕໍ່',
            'phone_number': 'ເບີໂທ',
            'email': 'ອີເມວ',
            'company_address': 'ທີ່ຢູ່',
        }

    def __init__(self, *args, **kwargs):
        super(CustomersModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control w3-input w3-border w3-round-large w3-margin-bottom'
