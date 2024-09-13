from django import forms
from django.forms import ModelForm
from apps.leave.models import LeaveRequest, LeaveType, EmployeeLeave, LeaveApproval
from apps.employee.models import Employee

class LeaveTypeForm(ModelForm):
    class Meta:
        model = LeaveType
        fields = ['leave_type', 'number_of_leave_days', 'carryover_unused']

class LeaveRequestForm(ModelForm):
    class Meta:
        model = LeaveRequest
        fields = '__all__'

        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(LeaveRequestForm, self).__init__(*args, **kwargs)
        self.fields['days_taken'].widget.attrs['readonly'] = True
        if user is not None:
            employee = user.employee
            self.fields['leave_type'].queryset = EmployeeLeave.objects.filter(employee__user=user)
            # self.fields['leave_type'].initial = "employee_leave.leave_type"
            self.fields['acting_staff'].queryset = Employee.objects.filter(office_department = employee.office_department.department.id)
            # self.fields['supervisor'].queryset = Employee.objects.filter(employee__supervisor = employee.supervisor)
            self.fields['supervisor'].initial = employee.supervisor
            self.fields['supervisor'].widget = forms.HiddenInput()
            self.fields['employee'].queryset = Employee.objects.filter(user = user)
            self.fields['employee'].initial = employee
            self.fields['employee'].widget = forms.HiddenInput()
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date:
            cleaned_data['days_taken'] = (end_date - start_date).days + 1
        return cleaned_data


class EmployeeLeaveForm(ModelForm):
    class Meta:
        model = EmployeeLeave
        fields = ['employee','leave_type', 'leave_balance', 'leave_status']
    
    def __init__(self, *args, **kwargs):
        super(EmployeeLeaveForm, self).__init__(*args, **kwargs)
        self.fields['leave_balance'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super().clean()
        leave_type = cleaned_data.get('leave_type')
        if leave_type:
            cleaned_data['leave_balance'] = leave_type.number_of_leave_days  # Assuming `default_days` is a field in LeaveType model
        return cleaned_data

    

class LeaveApprovalForm(ModelForm):
    class Meta:
        model = LeaveApproval
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(LeaveApprovalForm, self).__init__(*args, **kwargs)
        self.fields['leave_approved_by'].widget.attrs['readonly'] = True
        self.fields['leave_approved_by'].widget = forms.HiddenInput()
        

class EmployeeLeaveSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        # label='Search by Name',
        widget=forms.TextInput(attrs={'placeholder': 'Search by name...'})
)
    
class EmployeeLeaveFilterForm(forms.Form):
    LEAVE_FILTER = [
        ('all', 'All Leave'),
        ('my_leave', 'My Leave'),
    ]
    leave_list = forms.ChoiceField(
        choices=LEAVE_FILTER,
        required=False, 
    )
