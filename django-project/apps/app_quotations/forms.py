from django import forms
from django.forms import inlineformset_factory


#====================================== Import Models ======================================
from .models import QuotationInformationModel, QuotationItemsModel, AdditionalExpenses
from apps.app_customers.models import CustomersModel


#====================================== Class Forms ======================================
class QuotationInformationModelForm(forms.ModelForm):
    class Meta:
        model = QuotationInformationModel
        fields = ['create_date', 'expired_date', 'status']
        labels = {
            'create_date':'ວັນທີ່ອອກໃບສະເຫນີລາຄາ',
            'expired_date':'ວັນຫມົດອາຍຸ',
            'status':'ສະຖານະ',
        }
    def __init__(self, *args, **kwargs):
        super(QuotationInformationModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control w3-input w3-border w3-round-large w3-margin-bottom'
            if isinstance(field, forms.DateField):
                field.widget = forms.DateInput(attrs={
                    'class':'form-control w3-input w3-border w3-round-large w3-margin-bottom',
                    'type':'date'
                })


#====================================== Add form for Customer Model ======================================
class CustomersModelForm(forms.ModelForm):
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
        super(CustomersModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w3-input w3-border w3-round-large w3-margin-bottom',
                'placeholder': field.label
            })

#====================================== Class Addtional Expenses Form using on inline formset======================================
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

#====================================== Class Quotation Item Form Form using on inline formset======================================
class QuotationItemsForm(forms.ModelForm):
    class Meta:
        model = QuotationItemsModel
        fields = ['product_name', 'price', 'qty', 'period']
        labels = {
            'product_name': 'ສິນຄ້າ',
            'price': 'ລາຄາ',
            'qty': 'ຈຳນວນ',
            'period': 'ໄລຍະເວລາ',
        }
    def __init__(self, *args, **kwargs):
        super(QuotationItemsForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w3-input w3-border w3-round-large w3-margin-bottom',
                'placeholder': field.label
            })

        if 'DELETE' in self.fields:
            self.fields['DELETE'].label = 'ລຶບ'

#====================================== Additional Expenses Formset ======================================
AdditionalExpensesFormSet = inlineformset_factory(
    QuotationInformationModel,
    AdditionalExpenses,
    form=AdditionalExpensesForm,
    extra=1,
    max_num=1,
    can_delete=False
)

#====================================== Inline FormSet for QuotationItemsModel ======================================
QuotationItemsFormSet = inlineformset_factory(
    QuotationInformationModel,
    QuotationItemsModel,
    form=QuotationItemsForm,
    extra=1,
    can_delete=True,
)