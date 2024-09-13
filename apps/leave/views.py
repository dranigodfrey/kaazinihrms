from django.shortcuts import render, redirect
from apps.leave.models import LeaveType, LeaveRequest, EmployeeLeave, LeaveApproval
from apps.leave.forms import LeaveTypeForm, LeaveRequestForm, EmployeeLeaveForm, LeaveApprovalForm, EmployeeLeaveSearchForm,EmployeeLeaveFilterForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from apps.account.decorators import group_required
from .resources import EmployeeLeaveResource


# Export Employees Leaves 
@login_required
@group_required('Admin', 'HR Admin')
def export_leaves_to_excel(request):
    employee_resource = EmployeeLeaveResource()
    dataset = employee_resource.export()
    response = HttpResponse(dataset.export('xlsx'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="leaves.xlsx"'
    return response

# leave type views
@login_required
def get_leave_data(request):
    employee_leaves = EmployeeLeave.objects.filter(employee__user__id = request.user.id)

    leave_data = []
    for leave in employee_leaves:
        leave_data.append({
            'leave_type': str(leave.leave_type),
            'leave_taken': leave.leave_taken, 
            'leave_balance': leave.leave_balance
    })
    return JsonResponse({'leave_data': leave_data})

@login_required
def leave_dashboard(request):
    user_roles = ['admin', 'manager','hr','supervisee']
   
    employee_leave_request = LeaveRequest.objects.filter(employee__user__id = request.user.id)
    leave_request_received = LeaveApproval.objects.filter(Q(leave_request_status = 'pending') & Q(leave_approved_by__user__id = request.user.id)).count()
    leave_types = LeaveType.objects.all()

    pending_leaves = LeaveApproval.objects.filter(Q(leave_request_status = 'pending') & Q(leave_requested_by__user__id = request.user.id)).count()
    approved_leaves = LeaveApproval.objects.filter(Q(leave_request_status='approved') & Q(leave_requested_by__user__id = request.user.id)).count()
    rejected_leaves = LeaveApproval.objects.filter(Q(leave_request_status='rejected') & Q(leave_requested_by__user__id = request.user.id)).count()

    context = {
        'employee_leave_request': employee_leave_request,
        'leave_types': leave_types,
        'pending_leaves': pending_leaves,
        'approved_leaves': approved_leaves,
        'rejected_leaves': rejected_leaves,
        'user_roles': user_roles,
        'leave_request_received':leave_request_received,
    }
    return render(request, template_name='leave/leave_dashboard.html', context = context)

@login_required
def approve_leave(request):
    
    leave_request_received = LeaveApproval.objects.filter(Q(leave_request_status = 'pending') & Q(leave_approved_by__user__id = request.user.id))
    leave_request_approved = LeaveApproval.objects.filter(Q(leave_request_status = 'approved') & Q(leave_approved_by__user__id = request.user.id))
    
    context = {
        'leave_request_received':leave_request_received,
        'leave_request_approved': leave_request_approved,
    }
    return render(request, template_name='leave/approve_leave.html', context = context)


@login_required
def employee_leave_approved(request):
    search_form = EmployeeLeaveSearchForm(request.GET or None)
    filter_form = EmployeeLeaveFilterForm(request.GET or None)
    if request.user.user_role in ['admin', 'hr_admin', 'manager']:
        employee_leave_approved = LeaveApproval.objects.filter(leave_request_status = 'approved')
        if search_form.is_valid():
            search_query = search_form.cleaned_data.get('search')

            # Filter by search query on user's first name and last name
            if search_query:
                employee_leave_approved = employee_leave_approved.filter(
                (Q(Q(leave_requested_by__user__first_name__icontains = search_query) | 
                    Q(leave_requested_by__user__second_name__icontains = search_query)))
                )

            if filter_form.is_valid():
                search_query = filter_form.cleaned_data.get('search')
                leave_list = filter_form.cleaned_data['leave_list']

                # Filter by contract status
                if leave_list == 'my_leave':
                    employee_leave_approved = LeaveApproval.objects.filter(Q(leave_request_status = 'approved') & Q(leave_requested_by__user__id = request.user.id))
                # else:
                #     employee_contracts = employee_contracts.all()
    else: 
        employee_leave_approved = LeaveApproval.objects.filter(Q(leave_request_status = 'approved') & Q(leave_requested_by__user__id = request.user.id))
    
    context = {
        'employee_leave_approved':employee_leave_approved,
        'search_form': search_form,
        'filter_form': filter_form,
    }
    return render(request, template_name='leave/employee_leave_approved.html', context = context)


@login_required
def employee_leave_rejected(request):
    search_form = EmployeeLeaveSearchForm(request.GET or None)
    filter_form = EmployeeLeaveFilterForm(request.GET or None)
    if request.user.user_role in ['admin', 'hr_admin', 'manager']:
        employee_leave_rejected = LeaveApproval.objects.filter(leave_request_status = 'rejected')
        if search_form.is_valid():
            search_query = search_form.cleaned_data.get('search')

            # Filter by search query on user's first name and last name
            if search_query:
                employee_leave_rejected = employee_leave_rejected.filter(
                (Q(Q(leave_requested_by__user__first_name__icontains = search_query) | 
                    Q(leave_requested_by__user__second_name__icontains = search_query)))
                )

            if filter_form.is_valid():
                search_query = filter_form.cleaned_data.get('search')
                leave_list = filter_form.cleaned_data['leave_list']

                # Filter by contract status
                if leave_list == 'my_leave':
                    employee_leave_rejected = LeaveApproval.objects.filter(Q(leave_request_status = 'rejected') & Q(leave_requested_by__user__id = request.user.id))
                # else:
                #     employee_contracts = employee_contracts.all()
    else: 
        employee_leave_rejected = LeaveApproval.objects.filter(Q(leave_request_status = 'rejected') & Q(leave_requested_by__user__id = request.user.id))
    
    context = {
        'employee_leave_rejected':employee_leave_rejected,
        'search_form': search_form,
        'filter_form': filter_form,
    }
    return render(request, template_name='leave/employee_leave_rejected.html', context = context)


@login_required
def employee_leave_pending(request):
    search_form = EmployeeLeaveSearchForm(request.GET or None)
    filter_form = EmployeeLeaveFilterForm(request.GET or None)
    if request.user.user_role in ['admin', 'hr_admin', 'manager']:
        employee_leave_pending = LeaveApproval.objects.filter(leave_request_status = 'pending')
        if search_form.is_valid():
            search_query = search_form.cleaned_data.get('search')

            # Filter by search query on user's first name and last name
            if search_query:
                employee_leave_pending = employee_leave_pending.filter(
                (Q(Q(leave_requested_by__user__first_name__icontains = search_query) | 
                    Q(leave_requested_by__user__second_name__icontains = search_query)))
                )

            if filter_form.is_valid():
                search_query = filter_form.cleaned_data.get('search')
                leave_list = filter_form.cleaned_data['leave_list']

                # Filter by contract status
                if leave_list == 'my_leave':
                    employee_leave_pending = LeaveApproval.objects.filter(Q(leave_request_status = 'pending') & Q(leave_requested_by__user__id = request.user.id))
                # else:
                #     employee_contracts = employee_contracts.all()
    else:  
        employee_leave_pending = LeaveApproval.objects.filter(Q(leave_request_status = 'pending') & Q(leave_requested_by__user__id = request.user.id))
    
    context = {
        'employee_leave_pending':employee_leave_pending,
        'search_form': search_form,
        'filter_form': filter_form,
    }
    return render(request, template_name='leave/employee_leave_pending.html', context = context)


@login_required
@group_required('Admin', 'HR Admin', 'Manager')
def update_leave_approval(request, pk):
    leave_approval = LeaveApproval.objects.get(id = pk)
    # suppervisor = LeaveRequest.objects.filter(employee__user__id = request.user.id)
    if request.method == 'POST':
        form = LeaveApprovalForm(request.POST, request.FILES, instance = leave_approval)
        if form.is_valid():
            form.save()
            return redirect('approve_leave')
        else:
            return HttpResponse('Failed to update leave approval record.')
    else:
        form = LeaveApprovalForm(instance = leave_approval)
    context = {
        'form': form
    }
    return render(request, template_name='leave/add_leave_approval.html', context = context)


@login_required
@group_required('Admin', 'HR Admin')
def leave_type(request):
    leave_types = LeaveType.objects.all()
    context = {
        'leave_types': leave_types,
    }
    return render(request, template_name='leave/leave_type.html', context = context)

@login_required
@group_required('Admin', 'HR Admin')
def add_leave_type(request):
    if request.method =='POST':
        form = LeaveTypeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('leave_type')
    else:
         form = LeaveTypeForm()
    context = {
        'form': form
    }
    return render(request, template_name='leave/add_leave_type.html', context = context)

@login_required
@group_required('Admin', 'HR Admin')
def update_leave_type(request, pk):
    leave_type = LeaveType.objects.get(id = pk)
    if request.method == 'POST':
        form = LeaveTypeForm(request.POST, request.FILES, instance = leave_type)
        if form.is_valid():
            form.save()
            return redirect('leave_type')
        else:
            return HttpResponse('Failed to update leave_type record.')
    else:
        form = LeaveTypeForm(instance = leave_type)
    context = {
        'form': form
    }
    return render(request, template_name='leave/add_leave_type.html', context = context)

@login_required
@group_required('Admin', 'HR Admin')
def delete_leave_type(request, pk):
    leave_type = LeaveType.objects.get(id = pk)
    if request.method == 'POST':
        leave_type.delete()
        return redirect('leave_type')
    context = {
        'leave_type': leave_type
    }
    return render(request, template_name='leave/delete_leave_type.html', context = context)

# Employee leave views
@login_required
@group_required('Admin', 'HR Admin')
def employee_leave(request):
    employee_leaves = EmployeeLeave.objects.all()
    search_form = EmployeeLeaveSearchForm(request.GET or None)
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search')

        # Filter by search query on user's first name and last name
        if search_query:
            employee_leaves = employee_leaves.filter(
               (Q(Q(employee__user__first_name__icontains = search_query) | 
                Q(employee__user__second_name__icontains = search_query)))
            )

    context = {
        'employee_leaves': employee_leaves,
        'search_form': search_form,
    }
    return render(request, template_name='leave/employee_leave.html', context = context)

@login_required
@group_required('Admin', 'HR Admin')
def add_employee_leave(request):
    if request.method =='POST':
        form = EmployeeLeaveForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('employee_leave')
    else:
         form = EmployeeLeaveForm()
    context = {
        'form': form
    }
    return render(request, template_name='leave/add_employee_leave.html', context = context)

@login_required
@group_required('Admin', 'HR Admin')
def update_employee_leave(request, pk):
    employee_leave = EmployeeLeave.objects.get(id = pk)
    if request.method == 'POST':
        form = EmployeeLeaveForm(request.POST, request.FILES, instance = employee_leave)
        if form.is_valid():
            form.save()
            return redirect('employee_leave')
        else:
            return HttpResponse('Failed to update employee_leave record.')
    else:
        form = EmployeeLeaveForm(instance = employee_leave)
    context = {
        'form': form
    }
    return render(request, template_name='leave/add_employee_leave.html', context = context)

@login_required
@group_required('Admin', 'HR Admin')
def delete_employee_leave(request, pk):
    employee_leave = EmployeeLeave.objects.get(id = pk)
    if request.method == 'POST':
        employee_leave.delete()
        return redirect('employee_leave')
    context = {
        'employee_leave': employee_leave
    }
    return render(request, template_name='leave/delete_employee_leave.html', context = context)

# Employee leave request views
@login_required
def leave_request(request):
    if request.user.user_role in ['admin', 'hr_admin']:
        leave_requests = LeaveApproval.objects.filter( Q(leave_request_status = "approved")|Q(leave_request_status = "rejected"))
    else:
        leave_requests = LeaveApproval.objects.filter(Q(leave_requested_by__user__id = request.user.id))
   
    context = {
        'leave_requests': leave_requests,
    }
    return render(request, template_name='leave/leave_history.html', context = context)

@login_required
def add_leave_request(request):
    if request.method =='POST':
        form = LeaveRequestForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('pending_leave')
    else:
         form = LeaveRequestForm(user=request.user)
    context = {
        'form': form
    }
    return render(request, template_name='leave/add_leave_request.html', context = context)


@login_required
def update_leave_request(request, pk):
    leave_request = LeaveRequest.objects.get(id = pk)
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST, request.FILES, instance = leave_request, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('pending_leave')
        else:
            return HttpResponse('Failed to update leave_request record.')
    else:
        form = LeaveRequestForm(instance = leave_request, user=request.user)
    context = {
        'form': form
    }
    return render(request, template_name='leave/add_leave_request.html', context = context)


@login_required
def delete_leave_request(request, pk):
    leave_request = LeaveRequest.objects.get(id = pk)
    if request.method == 'POST':
        leave_request.delete()
        return redirect('leave_request')
    context = {
        'leave_request': leave_request
    }
    return render(request, template_name='leave/delete_leave_request.html', context = context)
