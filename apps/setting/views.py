from django.shortcuts import render, redirect
from apps.setting.models import Holiday, WorkSchedule
from apps.setting.forms import HolidayForm, WorkScheduleForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def setting(request):
    holidays = Holiday.objects.all()
    workschedules = WorkSchedule.objects.all()
    context = {
        'holidays': holidays,
        'workschedules': workschedules,
    }
    return render(request, template_name='setting/setting.html', context=context)

# Holiday views 
@login_required
def holiday(request):
    holidays = Holiday.objects.all()
    context = {
        'holidays': holidays,
    }
    return render(request, template_name='setting/holiday.html', context=context)

@login_required
def add_holiday(request):
    if request.method =='POST':
        form = HolidayForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('holiday')
    else:
         form = HolidayForm()
    context = {
        'form': form
    }
    return render(request, template_name='setting/add_holiday.html', context = context)

@login_required
def update_holiday(request, pk):
    holiday = Holiday.objects.get(id = pk)
    if request.method == 'POST':
        form = HolidayForm(request.POST, request.FILES, instance = holiday)
        if form.is_valid():
            form.save()
            return redirect('holiday')
        else:
            return HttpResponse('Failed to update holiday record.')
    else:
        form = HolidayForm(instance = holiday)
    context = {
        'form': form
    }
    return render(request, template_name='setting/add_holiday.html', context = context)

@login_required
def delete_holiday(request, pk):
    holiday = Holiday.objects.get(id = pk)
    if request.method == 'POST':
        holiday.delete()
        return redirect('holiday')
    context = {
        'holiday': holiday
    }
    return render(request, template_name='setting/delete_holiday.html', context = context)

# WorkSchedule views 
@login_required
def workschedule(request):
    workschedules = WorkSchedule.objects.all()
    context = {
        'workschedules': workschedules,
    }
    return render(request, template_name='setting/workschedule.html', context=context)

@login_required
def add_workschedule(request):
    if request.method =='POST':
        form = WorkScheduleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('workschedule')
    else:
         form = WorkScheduleForm()
    context = {
        'form': form
    }
    return render(request, template_name='setting/add_workschedule.html', context = context)

@login_required
def update_workschedule(request, pk):
    workschedule = WorkSchedule.objects.get(id = pk)
    if request.method == 'POST':
        form = WorkScheduleForm(request.POST, request.FILES, instance = workschedule)
        if form.is_valid():
            form.save()
            return redirect('workschedule')
        else:
            return HttpResponse('Failed to update workschedule record.')
    else:
        form = WorkScheduleForm(instance = workschedule)
    context = {
        'form': form
    }
    return render(request, template_name='setting/add_workschedule.html', context = context)

@login_required
def delete_workschedule(request, pk):
    workschedule = WorkSchedule.objects.get(id = pk)
    if request.method == 'POST':
        workschedule.delete()
        return redirect('workschedule')
    context = {
        'workschedule': workschedule
    }
    return render(request, template_name='setting/delete_workschedule.html', context = context)
