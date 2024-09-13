from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.company.models import Company, Office, Department, OfficeDepartment
from apps.leave.models import LeaveType
from apps.employee.models import EmployeeTitle
from apps.tenant.models import Client
from django.contrib.auth.models import Group


@receiver(post_save, sender=Client)
def create_initial_tenant_data(sender, instance, created, **kwargs):
    if created and Client.schema_name ==  'public':
            Company.objects.get_or_create(
                company_name = instance.name,
                company_type = "private company",
                company_email = f"{instance.name}@{instance.name}.com",
                company_phone = "+256000000000",

            )

            # Create default user groups
            groups = ["Admin", "HR Admin", "Manager", "Employee"]
            for group in groups:
                Group.objects.get_or_create(name=group)
            
            # Create default leave type
            LeaveType.objects.get_or_create(
                leave_type="Annual Leave",
                number_of_leave_days = 21,
                carryover_unused = True
            )

            # Create default employee title
            EmployeeTitle.objects.get_or_create(
                title_name="example title",
                education_level="masters degree",
            )

            # Create default office
            Office.objects.get_or_create(
                office_name="Head Office", 
                country = "Uganda",
                district = "kampala",

            )

            # Create default department
            Department.objects.get_or_create(
                department_name = "Human Resource",
            )

            # assign default office and department
            OfficeDepartment.objects.get_or_create(
                office = 1, 
                department = 1
            )                
