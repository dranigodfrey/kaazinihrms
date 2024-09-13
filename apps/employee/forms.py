from django import forms
from django.forms import ModelForm
from apps.company.models import Office, Department
from apps.employee.models import Employee, EmployeeContract, EmployeeTitle

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

        widgets = {
            'employee_email': forms.EmailInput(attrs={'placeholder': 'email@company.com', 'type':'email'}),
            'employee_dob': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            initial = kwargs['initial']
            if 'user' in initial:
                user = initial['user']
                self.fields['user'].initial = user
                self.fields['user'].widget = forms.HiddenInput()
                # self.fields['user'].initial = user.username

class EmployeeProfileForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['profile_pic']
        widgets = {
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control-file'},),
        }
        labels = {
            'profile_pic': '',
        }
          

class EmployeeContractForm(ModelForm):
    class Meta:
        model = EmployeeContract
        fields = '__all__'

        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'probation_start': forms.DateInput(attrs={'type': 'date'}),
            'probation_end': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super(EmployeeContractForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            initial = kwargs['initial']
            if 'employee' in initial:
                employee = initial['employee']


class EmployeeTitleForm(ModelForm):
    class Meta:
        model = EmployeeTitle
        fields = '__all__'

class EmployeeFilterForm(forms.Form):
    office = forms.ModelChoiceField(
        queryset=Office.objects.all(),
        required=False,
        # label='Filter by Office',
        empty_label='All Offices'
    )
    office_department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        # label='Filter by Department',
        empty_label='All Departments'
    )

class EmployeeSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        # label='Search by Name',
        widget=forms.TextInput(attrs={'placeholder': 'Search by name...'})
    )


class EmployeeContractFilterForm(forms.Form):
    CONTRACT_STATUS = [
        ('all', 'All Contracts'),
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    contract_status = forms.ChoiceField(
        choices=CONTRACT_STATUS,
        required=False, 
    )


    job_title = forms.ModelChoiceField(
        queryset=EmployeeTitle.objects.all(),
        required=False,
        # label='Filter by Job title',
        empty_label='All Titles'
    )

