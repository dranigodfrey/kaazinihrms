from django.dispatch import receiver
from django.db.models.signals import post_save
from apps.leave.models import EmployeeLeave, LeaveRequest, LeaveApproval
from apps.notification.models import Notification


@receiver(post_save, sender=LeaveRequest)
def create_leave_approval(sender, instance, created, **kwargs):
    if created:
        LeaveApproval.objects.create(
            leave_request = instance,
            leave_requested_by = instance.employee,
            leave_approved_by = instance.supervisor
        )


@receiver(post_save, sender=LeaveRequest)
def notify_supervisor(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient = instance.supervisor,
            sender = instance.employee,
            message = f'{instance.employee} has requested for {instance.leave_type.leave_type}, Please review.',
            status = 'unread'
        )


@receiver(post_save, sender=LeaveApproval)
def notify_employee(sender, instance, created, **kwargs):
    if not instance.is_pending():
        if instance.leave_request_status == 'approved':
            message  = f'Your {instance.leave_request.leave_type} request has been approved.'
        else:
            message  = f'Your {instance.leave_request.leave_type} request has been rejected.'
        Notification.objects.create(
            recipient = instance.leave_requested_by,
            sender = instance.leave_approved_by,
            message = message,
            status = 'unread'
        )

@receiver(post_save, sender=LeaveApproval)
def update_leave_balance(sender, instance, created, **kwargs):
    if not created and instance.leave_request_status == 'approved':
        leave_id = instance.leave_request.leave_type.id
        employee_leave = EmployeeLeave.objects.get(id=leave_id)
        employee_leave.leave_balance = instance.leave_request.leave_type.leave_balance - instance.leave_request.leave_duration
        employee_leave.leave_taken = instance.leave_request.leave_type.leave_balance - employee_leave.leave_balance
        employee_leave.leave_taken_date = instance.leave_request.start_date
        employee_leave.save(update_fields=['leave_balance', 'leave_taken', 'leave_taken_date'])
        print('Your leave request has been approved')

