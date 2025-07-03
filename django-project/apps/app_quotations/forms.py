from django import forms
from django.forms import modelformset_factory
from apps.app_customers.models import CustomersModel
from .models import QuotationsModel, AdditionalExpensesModel


class QuotationsModelForm(forms.ModelForm):
    class Meta:
        model = QuotationsModel
        fields = ['product_name', 'price', 'qty', 'period', 'status','create_at','expired_at']
        labels = {
            'product_name': 'ສິນຄ້າ',
            'price': 'ລາຄາ',
            'qty': 'ຈຳນວນ',
            'period': 'ໄລຍະເວລາ',
            'status': 'ສະຖານະ',
            'create_at': 'ວັນທີອອກ',
            'expired_at': 'ວັນທີຫມົດ'
        }

    def __init__(self, *args, **kwargs):
        super(QuotationsModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control w3-input w3-border w3-round w3-margin-bottom'

            # Check if the field is a DateField
            if isinstance(field, forms.DateField):
                field.widget = forms.DateInput(attrs={
                    'class':'form-control w3-input w3-border w3-round w3-margin-bottom',
                    'type':'date'
                })
#Inline Model Form Set
QuotationsModelFormSet = modelformset_factory(QuotationsModel, form=QuotationsModelForm, extra=1, can_delete=True)


###Additional ExpensesModelForm
class AdditionalExpensesModelForm(forms.ModelForm):
    class Meta:
        model = AdditionalExpensesModel
        fields = [
            'it_service_percent',
            'vat_percent',
            'exchange_rate'
        ]
        labels = {
            'it_service_percent': 'ຄ່າບໍລະການ IT',
            'vat_percent': 'ອາກອນມູນຄ່າເພີ່ມ',
            'exchange_rate': 'ອັດຕາແລກປ່ຽນ'
        }
    def __init__(self, *args, **kwargs):
        super(AdditionalExpensesModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control w3-input w3-border w3-round w3-margin-bottom'