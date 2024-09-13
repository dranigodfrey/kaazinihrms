from django.shortcuts import render, redirect
from apps.company.models import Company, Office, Department, OfficeDepartment
from apps.company.forms import CompanyForm, DepartmentForm, OfficeForm, OfficeDepartmentForm
from apps.employee.models import Employee, EmployeeContract
from apps.leave.models import LeaveRequest, LeaveApproval
from django.http import HttpResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from apps.account.decorators import group_required



User = get_user_model()

# Employee detail views
@login_required
def employee_gender_data(request):
     # Aggregate gender counts
    gender_data = Employee.objects.values('user__sex').annotate(count=Count('user__sex'))
    
    # Calculate the total number of employees
    total_count = sum(entry['count'] for entry in gender_data)

    # Prepare the response data
    response_data = {
        'labels': [entry['user__sex'].capitalize() for entry in gender_data],
        'counts': [entry['count'] for entry in gender_data],
        'total_count': total_count  # Include total count
    }
    return JsonResponse(response_data)

def employee_gender_chart(request):
    return render(request, 'main_dashboard.html')


@login_required
def employee_title_data(request):
    # Aggregate the data: count of employees by title
    title_data = EmployeeContract.objects.values('title__title_name').annotate(count=Count('id')).order_by('-count')

    # Prepare the data for JSON response
    data = {
        'titles': [entry['title__title_name'] for entry in title_data],
        'counts': [entry['count'] for entry in title_data]
    }

    return JsonResponse(data)


@login_required
def employee_department_data(request):
    # Aggregate the data: count of employees by department
    department_data = Employee.objects.values('office_department__department__department_name').annotate(count=Count('id')).order_by('-count')

    # Prepare the data for JSON response
    data = {
        'departments': [entry['office_department__department__department_name'] for entry in department_data],
        'counts': [entry['count'] for entry in department_data]
    }

    return JsonResponse(data)


#Main Dashboard
@login_required
# @group_required('Admin', 'HR Admin', 'Manager')
def main_dashboard(request):
    # if request.user.is_superuser:
    companies = Company.objects.all()
    employees = Employee.objects.all()
    total_employees = Employee.objects.count()
    leave_request = LeaveRequest.objects.all()
    leave_request_pending = LeaveApproval.objects.filter(leave_request_status = 'pending').count()
    leave_started = LeaveApproval.objects.filter(leave_request_status = 'approved').count()
    leave_up_coming = LeaveApproval.objects.filter(leave_request_status = 'approved').count()
    leave_request_rejected = LeaveApproval.objects.filter(leave_request_status = 'rejected').count()
    # else:
    #     companies = Company.objects.filter(id = request.user.employee.company.id)

    context = {
        'companies': companies,
        'employees': employees,
        'leave_request': leave_request,
        'leave_request_pending': leave_request_pending,
        'leave_started': leave_started,
        'leave_request_rejected': leave_request_rejected,
        'leave_up_coming': leave_up_coming,
        'total_employees':total_employees
    }
    return render(request, template_name='company/main_dashboard.html', context=context)


# company view section
@login_required
@group_required('Admin')
def company(request):
    if request.user.is_superuser:
        companies = Company.objects.all()
        officies = Office.objects.all()
        departments = Department.objects.all()
    else:
        companies = Company.objects.filter(id = request.user.employee.id)
    context = {
        'companies': companies
    }
    return render(request, template_name='company/company.html', context=context)

@login_required
@group_required('Admin')
def add_company(request):
    if request.method =='POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('company')
    else:
         form = CompanyForm()
    context = {
        'form': form
    }
    return render(request, template_name='company/add_company.html', context = context)

@login_required
@group_required('Admin')
def update_company(request, pk):
    company = Company.objects.get(id = pk)
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance = company)
        if form.is_valid():
            form.save()
            return redirect('company')
        else:
            return HttpResponse('Failed to update company record.')
    else:
        form = CompanyForm(instance = company)
    context = {
        'form': form
    }
    return render(request, template_name='company/add_company.html', context = context)

@login_required
@group_required('Admin')
def delete_company(request, pk):
    company = Company.objects.get(id = pk)
    if request.method == 'POST':
        company.delete()
        return redirect('company')
    context = {
        'company': company
    }
    return render(request, template_name='company/delete_company.html', context = context)

# Office view section
@login_required
@group_required('Admin')
def office (request):
    officies = Office.objects.all()
    context = {
        'officies': officies,
    }
    return render(request, template_name='company/office.html', context=context)

@login_required
@group_required('Admin')
def add_office(request):
    if request.method =='POST':
        form = OfficeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('office')
    else:
         form = OfficeForm()
    context = {
        'form': form
    }
    return render(request, template_name='company/add_office.html', context = context)

@login_required
@group_required('Admin')
def update_office(request, pk):
    office = Office.objects.get(id = pk)
    if request.method == 'POST':
        form = OfficeForm(request.POST, request.FILES, instance = office)
        if form.is_valid():
            form.save()
            return redirect('office')
        else:
            return HttpResponse('Failed to update office record.')
    else:
        form = OfficeForm(instance = office)
    context = {
        'form': form
    }
    return render(request, template_name='company/add_office.html', context = context)

@login_required
@group_required('Admin')
def delete_office(request, pk):
    office = Office.objects.get(id = pk)
    if request.method == 'POST':
        office.delete()
        return redirect('office')
    context = {
        'office': office
    }
    return render(request, template_name='company/delete_office.html', context = context)

# Department view section
@login_required
@group_required('Admin')
def department (request):
    departments = Department.objects.all()
    context = {
        'departments': departments,
    }
    return render(request, template_name='company/department.html', context=context)

@login_required
@group_required('Admin')
def add_department(request):
    if request.method =='POST':
        form = DepartmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('department')
    else:
         form = DepartmentForm()
    context = {
        'form': form
    }
    return render(request, template_name='company/add_department.html', context = context)

@login_required
@group_required('Admin')
def update_department(request, pk):
    department = Department.objects.get(id = pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, request.FILES, instance = department)
        if form.is_valid():
            form.save()
            return redirect('department')
        else:
            return HttpResponse('Failed to update department record.')
    else:
        form = DepartmentForm(instance = department)
    context = {
        'form': form
    }
    return render(request, template_name='company/add_department.html', context = context)

@login_required
@group_required('Admin')
def delete_department(request, pk):
    department = Department.objects.get(id = pk)
    if request.method == 'POST':
        department.delete()
        return redirect('department')
    context = {
        'department': department
    }
    return render(request, template_name='company/delete_department.html', context = context)

# assign department to office views 

# Department view section
@login_required
@group_required('Admin')
def office_department (request):
    departments = OfficeDepartment.objects.all()
    context = {
        'departments': departments,
    }
    return render(request, template_name='company/office_department.html', context=context)

@login_required
@group_required('Admin')
def assign_office_department(request):
    if request.method =='POST':
        form = OfficeDepartmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('office_department')
    else:
         form = OfficeDepartmentForm()
    context = {
        'form': form
    }
    return render(request, template_name='company/assign_office_department.html', context = context)

@login_required
@group_required('Admin')
def update_office_department(request, pk):
    department = OfficeDepartment.objects.get(id = pk)
    if request.method == 'POST':
        form = OfficeDepartmentForm(request.POST, request.FILES, instance = department)
        if form.is_valid():
            form.save()
            return redirect('office_department')
        else:
            return HttpResponse('Failed to update department record.')
    else:
        form = OfficeDepartmentForm(instance = department)
    context = {
        'form': form
    }
    return render(request, template_name='company/assign_office_department.html', context = context)

