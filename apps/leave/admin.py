from django.contrib import admin
from apps.leave.models import LeaveRequest, EmployeeLeave, LeaveType, LeaveApproval


admin.site.register(LeaveRequest)
admin.site.register(EmployeeLeave)
admin.site.register(LeaveType)
admin.site.register(LeaveApproval)