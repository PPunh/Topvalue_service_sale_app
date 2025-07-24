# coding=utf-8
from django import forms
from django.forms import ModelForm, inlineformset_factory
from .models import InvoiceInformationModel, InvoiceItemsModel, AdditionalExpenses
from apps.app_customers.models import CustomersModel

class InvoiceInformationModelForm(forms.ModelForm):
    class Meta:
        model = InvoiceInformationModel
        fields = ['created_date', 'expired_date', 'status']
        labels = {
            'created_date': 'ວັນທີ່ອອກໃບສະເຫນີລາຄາ',
            'expired_date': 'ວັນຫມົດອາຍຸ',
            'status': 'ສະຖານະ',
        }

    def __init__(self, *args, **kwargs):
        super(InvoiceInformationModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control w3-input w3-border w3-round-large w3-margin-bottom'
            if isinstance(field, forms.DateField):
                field.widget = forms.DateInput(attrs={
                    'class':'form-control w3-input w3-border w3-round-large w3-margin-bottom',
                    'type':'date'
                })

class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = CustomersModel
        fields = ['company_name', 'contact_person_name', 'phone_number', 'email', 'company_address']
        labels = {
            'company_name': 'ບໍລິສັດ',
            'contact_person_name': 'ຜູ້ຕິດຕໍ່',
            'phone_number': 'ເບີໂທ',
            'email': 'ອີເມວ',
            'company_address': 'ທີ່ຢູ່ບໍລິສັດ',
        }

    def __init__(self, *args, **kwargs):
        super(CustomerModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w3-input w3-border w3-round-large w3-margin-bottom',
                'placeholder': field.label
            })

class AdditionalExpensesForm(forms.ModelForm):
    class Meta:
        model = AdditionalExpenses
        fields = ['it_service_percent', 'vat_percent', 'exchange_rate']
        labels = {
            'it_service_percent': 'IT Service (%)',
            'vat_percent': 'VAT (%)',
            'exchange_rate': 'ອັດຕາແລກປ່ຽນ',
        }

    def __init__(self, *args, **kwargs):
        super(AdditionalExpensesForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w3-input w3-border w3-round-large w3-margin-bottom',
                'placeholder': field.label
            })

class InvoiceItemsModelForm(forms.ModelForm):
    class Meta:
        model = InvoiceItemsModel
        fields = ['product_name', 'price', 'qty', 'period']
        labels = {
            'product_name': 'ສິນຄ້າ',
            'price': 'ລາຄາ',
            'qty': 'ຈຳນວນ',
            'period': 'ໄລຍະເວລາ',
        }

    def __init__(self, *args, **kwargs):
        super(InvoiceItemsModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w3-input w3-border w3-round-large w3-margin-bottom',
                'placeholder': field.label
            })
        if 'DELETE' in self.fields:
            self.fields['DELETE'].label = 'ລຶບ'

# Formsets
AdditionalExpensesFormSet = inlineformset_factory(
    InvoiceInformationModel,
    AdditionalExpenses,
    form=AdditionalExpensesForm,
    extra=1,
    max_num=1,
    can_delete=False
)

InvoiceItemsModelFormSet = inlineformset_factory(
    InvoiceInformationModel,
    InvoiceItemsModel,
    form=InvoiceItemsModelForm,
    extra=1,
    can_delete=True,
)
