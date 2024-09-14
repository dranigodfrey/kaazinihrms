from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.employee.models import Employee, EmployeeContract,EmployeeTitle
from apps.leave.models import LeaveApproval, LeaveRequest, LeaveType, EmployeeLeave
from apps.company.models import Office, Department, Company
from apps.setting.models import Holiday, WorkSchedule
from apps.account.models import CustomUser
from django.conf import settings


class Command(BaseCommand):
    help = 'Creates initial groups and assigns permissions for the HR system'

    def handle(self, *args, **kwargs):
        # Define roles and the permissions they should have
        roles_permissions = {
            'Admin': [
                # Admin has full access to all permissions
                ('add_customuser', 'account.CustomUser'),
                ('change_customuser', 'account.CustomUser'),
                ('delete_customuser', 'account.CustomUser'),
                ('view_customuser', 'account.CustomUser'),
                ('add_employee', 'employee.Employee'),
                ('change_employee', 'employee.Employee'),
                ('delete_employee', 'employee.Employee'),
                ('view_employee', 'employee.Employee'),
                ('add_employeetitle', 'employee.EmployeeTitle'),
                ('change_employeetitle', 'employee.EmployeeTitle'),
                ('delete_employeetitle', 'employee.EmployeeTitle'),
                ('view_employeetitle', 'employee.EmployeeTitle'),
                ('add_employeecontract', 'employee.EmployeeContract'),
                ('change_employeecontract', 'employee.EmployeeContract'),
                ('delete_employeecontract', 'employee.EmployeeContract'),
                ('view_employeecontract', 'employee.EmployeeContract'),
                ('add_leavetype', 'leave.LeaveType'),
                ('change_leavetype', 'leave.LeaveType'),
                ('delete_leavetype', 'leave.LeaveType'),
                ('view_leavetype', 'leave.LeaveType'),
                ('add_employeeleave', 'leave.EmployeeLeave'),
                ('change_employeeleave', 'leave.EmployeeLeave'),
                ('delete_employeeleave', 'leave.EmployeeLeave'),
                ('view_employeeleave', 'leave.EmployeeLeave'),
                ('add_leaverequest', 'leave.LeaveRequest'),
                ('change_leaverequest', 'leave.LeaveRequest'),
                ('delete_leaverequest', 'leave.LeaveRequest'),
                ('view_leaverequest', 'leave.LeaveRequest'),
                ('add_leaveapproval', 'leave.LeaveApproval'),
                ('change_leaveapproval', 'leave.LeaveApproval'),
                ('delete_leaveapproval', 'leave.LeaveApproval'),
                ('view_leaveapproval', 'leave.LeaveApproval'),
                ('add_company', 'company.Company'),
                ('change_company', 'company.Company'),
                ('delete_company', 'company.Company'),
                ('view_company', 'company.Company'),
                ('add_office', 'company.Office'),
                ('change_office', 'company.Office'),
                ('delete_office', 'company.Office'),
                ('view_office', 'company.Office'),
                ('add_department', 'company.Department'),
                ('change_department', 'company.Department'),
                ('delete_department', 'company.Department'),
                ('view_department', 'company.Department'),
                 ('add_workschedule', 'setting.WorkSchedule'),
                ('change_workschedule', 'setting.WorkSchedule'),
                ('delete_workschedule', 'setting.WorkSchedule'),
                ('view_workschedule', 'setting.WorkSchedule'),
                 ('add_holiday', 'setting.Holiday'),
                ('change_holiday', 'setting.Holiday'),
                ('delete_holiday', 'setting.Holiday'),
                ('view_holiday', 'setting.Holiday'),
                # Add more permissions as needed
            ],
            'HR Admin': [
                ('add_employee', 'employee.Employee'),
                ('change_employee', 'employee.Employee'),
                ('view_employee', 'employee.Employee'),
                ('add_leaverequest', 'leave.LeaveRequest'),
                ('change_leaverequest', 'leave.LeaveRequest'),
                ('view_leaverequest', 'leave.LeaveRequest'),
                ('add_leaveapproval', 'leave.LeaveApproval'),
                ('change_leaveapproval', 'leave.LeaveApproval'),
                ('view_leaveapproval', 'leave.LeaveApproval'),
                ('add_employeetitle', 'employee.EmployeeTitle'),
                ('change_employeetitle', 'employee.EmployeeTitle'),
                ('delete_employeetitle', 'employee.EmployeeTitle'),
                ('view_employeetitle', 'employee.EmployeeTitle'),
                ('add_employeecontract', 'employee.EmployeeContract'),
                ('change_employeecontract', 'employee.EmployeeContract'),
                ('view_employeecontract', 'employee.EmployeeContract'),
                ('add_leavetype', 'leave.LeaveType'),
                ('change_leavetype', 'leave.LeaveType'),
                ('view_leavetype', 'leave.LeaveType'),
                ('add_employeeleave', 'leave.EmployeeLeave'),
                ('change_employeeleave', 'leave.EmployeeLeave'),
                ('view_employeeleave', 'leave.EmployeeLeave'),
            ],
            'Manager': [
                ('view_employee', 'employee.Employee'),
                ('add_leaverequest', 'leave.LeaveRequest'),
                ('view_leaverequest', 'leave.LeaveRequest'),
                ('change_leaveapproval', 'leave.LeaveApproval'),
                ('view_leaveapproval', 'leave.LeaveApproval'),
            ],
            'Employee': [
                ('view_employee', 'employee.Employee'),
                ('add_leaverequest', 'leave.LeaveRequest'),
                ('view_leaverequest', 'leave.LeaveRequest'),
                ('view_leaveapproval', 'leave.LeaveApproval'),
            ],
        }

        for role, permissions in roles_permissions.items():
            group, created = Group.objects.get_or_create(name=role)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Group "{role}" created successfully'))
            else:
                self.stdout.write(f'Group "{role}" already exists')

            for perm_codename, model in permissions:
                try:
                    # Ensure model string is correctly formatted
                    if '.' not in model:
                        self.stdout.write(self.style.ERROR(f'Model format error: "{model}"'))
                        continue
                    
                    app_label, model_name = model.split('.')
                    content_type = ContentType.objects.get(app_label=app_label, model=model_name.lower())
                    permission = Permission.objects.get(codename=perm_codename, content_type=content_type)
                    group.permissions.add(permission)

                except ContentType.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'ContentType for model "{model}" does not exist.'))
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Permission "{perm_codename}" not found for model "{model}"'))

            self.stdout.write(self.style.SUCCESS(f'Permissions assigned to group "{role}"'))

        self.stdout.write(self.style.SUCCESS('All groups and permissions have been set up successfully.'))