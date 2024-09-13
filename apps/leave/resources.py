from import_export import resources
from .models import EmployeeLeave

class EmployeeLeaveResource(resources.ModelResource):

    class Meta:
        model = EmployeeLeave
        fields = ('id','employee__user__first_name', 'employee__user__second_name', 'leave_type__leave_type', 'leave_balance', 'leave_taken_date', 'leave_status',)
        export_order = ('id','employee__user__first_name', 'employee__user__second_name', 'leave_type__leave_type', 'leave_balance',  'leave_taken_date', 'leave_status',)
