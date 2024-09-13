from django import forms
from django.forms import ModelForm
from apps.setting.models import Holiday, WorkSchedule

class HolidayForm(ModelForm):
    class Meta:
        model = Holiday
        fields = '__all__'

class WorkScheduleForm(ModelForm):
    class Meta:
        model = WorkSchedule
        fields = '__all__'
