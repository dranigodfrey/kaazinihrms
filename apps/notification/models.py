from django.db import models
from apps.employee.models import Employee


class Notification(models.Model):
    NOTIFICATION_STATUS = (
        ('unread', 'Unread'),
        ('read', 'Read'),
    )
    recipient = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='notifications_received')
    sender = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='notifications_sent')
    message = models.TextField()
    status = models.CharField(max_length=10, choices=NOTIFICATION_STATUS, default='unread')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
