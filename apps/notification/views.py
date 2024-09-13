from django.shortcuts import render, redirect
from django.http import HttpResponse
from apps.notification.models import Notification
from apps.notification.forms import NotificationForm
from django.contrib.auth.decorators import login_required


@login_required
def notification(request):
    notifications = Notification.objects.all()
    context = {
        'notifications': notifications,
    }
    return render(request, template_name='notification/notification.html', context=context)

@login_required
def update_notification(request, pk):
    notification = Notification.objects.get(id = pk)
    if request.method == 'POST':
        form = NotificationForm(request.POST, request.FILES, instance = notification)
        if form.is_valid():
            form.save()
            return redirect('notification')
        else:
            return HttpResponse('Failed to update notification record.')
    else:
        form = NotificationForm(instance = notification)
    context = {
        'form': form
    }
    return render(request, template_name='notification/update_notification.html', context = context)

@login_required
def delete_notification(request, pk):
    notification = Notification.objects.get(id = pk)
    if request.method == 'POST':
        notification.delete()
        return redirect('notification')
    context = {
        'notification': notification
    }
    return render(request, template_name='notification/delete_notification.html', context = context)
