from django import forms
from django.forms import ModelForm
from apps.notification.models import Notification


class NotificationForm(ModelForm):
    class Meta:
        model = Notification
        fields = ['status']