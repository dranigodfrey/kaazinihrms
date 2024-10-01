from django.db import models
from apps.employee.models import Employee
from apps.setting.models import Holiday, WorkSchedule
import numpy as np


class LeaveType(models.Model):
    leave_type = models.CharField( max_length=150, unique=True)
    number_of_leave_days = models.IntegerField()
    carryover_unused = models.BooleanField()
    employee_leave = models.ManyToManyField(Employee, through='Employeeleave',  through_fields=('leave_type','employee'),related_name='employee_leaves')

    def __str__(self) -> str:
        return self.leave_type
    

class EmployeeLeave(models.Model):
    LEAVE_STATUS = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    leave_balance = models.IntegerField(blank=True, null=True) #calculated field type FloatField
    leave_taken = models.IntegerField(blank=True, null=True) #calculated field type FloatField
    leave_status = models.CharField(max_length=100, choices=LEAVE_STATUS)
    leave_taken_date = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = ('leave_type','employee')
    
    # def save(self, *args, **kwargs ):
    #     if self.leave_type.leave_type == 'Annual Leave':
    #         self.leave_balance = 0
    #     super(EmployeeLeave, self).save( *args, **kwargs)

    def __str__(self) -> str:
        return f'{self.leave_type.leave_type.title()}'


class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(EmployeeLeave, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date =models.DateField()
    days_taken = models.IntegerField(blank=True, null=True)
    acting_staff = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='acting_employee')
    employee_note = models.TextField() 
    supervisor = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_supervisor')
    leave_request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.leave_type.leave_type}'
    
    @property
    def leave_duration(self):
        holidays = Holiday.objects.all()
        holiday_dates = []
        for holiday in holidays:
            holiday_dates.append(holiday.holiday_date)
        return np.busday_count(self.start_date, self.end_date, holidays=holiday_dates) + 1
    
class LeaveApproval(models.Model):
    LEAVE_REQUEST_STATUS = (
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),

        )
    leave_requested_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_requested_employee')
    leave_request = models.ForeignKey(LeaveRequest, on_delete=models.CASCADE)
    leave_approved_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_approved_employee')
    supervisor_comment = models.TextField(blank=True, null=True)
    leave_request_status = models.CharField(max_length=100, choices=LEAVE_REQUEST_STATUS, default = 'pending')
    leave_approved_date = models.DateTimeField(auto_now_add=True)

    def is_pending(self):
        return self.leave_request_status == 'pending'
    def __str__(self) -> str:
        return f'{self.leave_requested_by} {self.leave_request}'

    