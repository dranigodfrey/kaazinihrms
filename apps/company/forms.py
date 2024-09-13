from django import forms
from django.forms import ModelForm
from apps.company.models import Company, Department, Office, OfficeDepartment

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

        widgets = {
            'company_email': forms.EmailInput(attrs={'placeholder': 'email@company.com'}),
            'company_phone': forms.NumberInput(attrs={'placeholder': '+256' }),
            'company_website': forms.URLInput(attrs={'placeholder': 'https://www.company.com' }),
        }

class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

class OfficeForm(ModelForm):
    class Meta:
        model = Office
        fields = '__all__'

class OfficeDepartmentForm(ModelForm):
    class Meta:
        model = OfficeDepartment
        fields = '__all__'