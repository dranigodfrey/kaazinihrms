from django.dispatch import receiver
from django.db.models.signals import post_save
from apps.employee.models import Employee
from django.conf import settings
from django.contrib.auth.models import Group
import os
from django.core.files import File
from django.contrib.auth import get_user_model
from apps.company.models import Office, Department, OfficeDepartment
from apps.leave.models import LeaveType
from apps.employee.models import EmployeeTitle

User = get_user_model()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_initial_user_data(sender, instance, created, **kwargs):
    if created:
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

            office = Office.objects.get(id=1)
            department = Department.objects.get(id=1)

          # assign default office and department
            OfficeDepartment.objects.get_or_create(
                office = office, 
                department = department
            )                
           

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_employee(sender, instance, created, **kwargs):
    """
    Signal handler function to create Employee instance.
    """
    if created:
        default_image_path = os.path.join(settings.MEDIA_ROOT, 'media/profile_picture/default_profile.png')
        employee = Employee.objects.create(user = instance)
        if os.path.exists(default_image_path):
            # Create Employee with default profile image
            with open(default_image_path, 'rb') as image_file:
                 employee.profile_pic.save('default_profile.png', File(image_file), save=True)
 


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def assign_user_to_group(sender, instance, created, **kwargs):
    if created:
        # Automatically assign user to group based on their role
        try:
            if instance.user_role == 'admin':
                group = Group.objects.get(name='Admin')
            elif instance.user_role == 'hr_admin':
                group = Group.objects.get(name='HR Admin')
            elif instance.user_role == 'manager':
                group = Group.objects.get(name='Manager')
            elif instance.user_role == 'employee':
                group = Group.objects.get(name='Employee')
            else:
                return  # Skip if no matching role

            instance.groups.add(group)
        except Group.DoesNotExist:
            # Handle case where the group does not exist
            print(f"Group {instance.user_role} does not exist. Please create it first.")
