from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Employee, EmployeeContract

class EmployeeResource(resources.ModelResource):
    supervisor_username = fields.Field(
        column_name='supervisor',
        attribute='supervisor',
        widget=ForeignKeyWidget(Employee, 'user__username')
    )
    class Meta:
        model = Employee
        fields = ('id','user__first_name', 'user__middle_name', 'user__second_name', 'user__sex', 'employee_dob', ' place_of_birth', 'marital_status', 'employee_email', 'employee_phone', 'home_town', 'office_department__office__office_name','office_department__department__department_name','supervisor_username', 'date_joined')
        export_order = ('id','user__first_name', 'user__middle_name', 'user__second_name', 'user__sex', 'employee_dob', ' place_of_birth', 'marital_status', 'employee_email', 'employee_phone', 'home_town','office_department__office__office_name', 'office_department__department__department_name','supervisor_username', 'date_joined')


class EmployeeContractResource(resources.ModelResource):

    class Meta:
        model = EmployeeContract
        fields = ('id','employee__user__first_name', 'employee__user__middle_name', 'employee__user__second_name', 'employee__user__sex', 'title__title_name',  'start_date', 'end_date', 'probation_start', 'probation_end', 'type_of_employement','type_of_commitment','contract_status')
        export_order = ('id','employee__user__first_name', 'employee__user__middle_name', 'employee__user__second_name', 'employee__user__sex', 'title__title_name', 'start_date', 'end_date', 'probation_start', 'probation_end', 'type_of_employement','type_of_commitment','contract_status')
