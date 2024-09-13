from django.dispatch import receiver
from django.db.models.signals import post_save
from apps.employee.models import Employee,EmployeeContract
from apps.leave.models import LeaveType, EmployeeLeave


@receiver(post_save, sender=Employee)
def assign_employee_leave_types(sender, instance, created, **kwargs):
    """
    Signal handler function to assign leave types when creating an Employee instance.
    """
    if created:
        # Get the gender from the Employee instance
        employee_sex = instance.user.sex
        
        # Query all leave types from the LeaveType model
        leave_types = LeaveType.objects.all()

        # Loop through each leave type and assign to the employee based on employee_sex
        for leave_type in leave_types:
            # Check if the leave type matches the employee_sex -specific leave type
            if employee_sex == 'female' and leave_type.leave_type == 'paternity leave':
                continue
                
            elif employee_sex == 'male' and leave_type.leave_type == 'maternity leave':
                continue
                
            else:
                # For other leave types or unspecified employee_sex, assign as usual
                EmployeeLeave.objects.create(employee=instance, leave_type=leave_type, leave_balance = leave_type.number_of_leave_days)

@receiver(post_save, sender=Employee)
def assign_employee_contract(sender, instance, created, **kwargs):
    if created:
        EmployeeContract.objects.create(employee=instance)
    else:
        employee_contract = EmployeeContract.objects.get(employee=instance)
        employee_contract.save()