from django.shortcuts import render, redirect, get_object_or_404
from apps.employee.models import Employee, EmployeeContract, EmployeeTitle
from apps.employee.forms import EmployeeForm, EmployeeSearchForm, EmployeeFilterForm, EmployeeContractForm, EmployeeTitleForm,EmployeeProfileForm,EmployeeContractFilterForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import get_user_model
from .resources import EmployeeResource, EmployeeContractResource
from apps.account.decorators import group_required


Users = get_user_model()

# Export Employees 
@login_required
@group_required('Admin', 'HR Admin')
def export_employees_to_excel(request):
    employee_resource = EmployeeResource()
    dataset = employee_resource.export()
    response = HttpResponse(dataset.export('xlsx'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="employees.xlsx"'
    return response

# Export Employees 
@login_required
@group_required('Admin', 'HR Admin')
def export_employee_contract_to_excel(request):
    employee_resource = EmployeeContractResource()
    dataset = employee_resource.export()
    response = HttpResponse(dataset.export('xlsx'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="employee contracts.xlsx"'
    return response


# Employee views
@login_required
def employee_profile(request):
    employee_active = Employee.objects.filter(user = request.user)
    if employee_active:
        employee  = get_object_or_404(Employee, user=request.user)
        employee_profile = Employee.objects.filter(user = request.user)
        employee_contract = EmployeeContract.objects.filter(employee__user = request.user)
        if request.method =='POST':
            form = EmployeeProfileForm(request.POST, request.FILES, instance=employee)
            if form.is_valid():
                form.save()
                return redirect('employee_profile')
        else:
            form = EmployeeProfileForm(instance=employee)
        context = {
            'employee_profile': employee_profile,
            'employee_contract': employee_contract,
            'form':form
        }
        return render(request, template_name='employee/employee_profile.html', context = context)
    else:
        return render(request, template_name='error_employee.html')
    
    
@login_required
def employee(request):
    employees = Employee.objects.select_related('user', 'office_department').all()
    filter_form = EmployeeFilterForm(request.GET or None)
    search_form = EmployeeSearchForm(request.GET or None)

    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search')

        # Filter by search query on user's first name and last name
        if search_query:
            employees = employees.filter(
               (Q(Q(user__first_name__icontains = search_query) | 
                Q(user__second_name__icontains = search_query)))
            )

    if filter_form.is_valid():
        search_query = filter_form.cleaned_data.get('search')
        office = filter_form.cleaned_data.get('office')
        department = filter_form.cleaned_data.get('office_department')

        # Filter by department's office
        if office:
            employees = employees.filter(office_department__office=office)

        # Filter by department
        if department:
            employees = employees.filter(office_department__department =department)
    
    context = {
        'employees': employees,
        'search_form': search_form,
        'filter_form': filter_form,
    }
    if request.user.user_role in ['admin', 'hr_admin']:
        return render(request, template_name='employee/employee.html', context = context)
    else:
        return render(request, template_name='employee/employee_2_.html', context = context)


@login_required
@group_required('Admin', 'HR Admin')
def user_list(request):
    users_without_employee = Employee.objects.filter(employee_email ="")
    context = {
        'employees': users_without_employee
    }
    return render(request, template_name='employee/new_employee.html', context=context)

@login_required
@group_required('Admin', 'HR Admin')
def add_employee(request):
    # user = get_object_or_404(Users, id = user_id)
    if request.method =='POST':
        form = EmployeeForm(request.POST, request.FILES,)
        if form.is_valid():
            # employee = form.save(commit=False)
            # employee.user = user
            form.save()
            return redirect('employee')
    else:
         form = EmployeeForm()
    context = {
        'form': form
    }
    return render(request, template_name='employee/add_employee.html', context = context)

@login_required
@group_required('Admin', 'HR Admin')
def update_employee(request, pk):
    employee = Employee.objects.get(id = pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance = employee)
        if form.is_valid():
            form.save()
            return redirect('user_list')
        else:
            return HttpResponse('Failed to update employee record.')
    else:
        form = EmployeeForm(instance = employee)
    context = {
        'form': form,
        'employee':employee
    }
    return render(request, template_name='employee/add_employee.html', context = context)

@login_required
@group_required('Admin', 'HR Admin')
def delete_employee(request, pk):
    employee = Employee.objects.get(id = pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee')
    context = {
        'employee': employee
    }
    return render(request, template_name='employee/delete_employee.html', context = context)

# Employee title views 
@login_required
@group_required('Admin', 'HR Admin')
def employee_title(request):
    employee_titles = EmployeeTitle.objects.all()
    context = {
        'employee_titles': employee_titles,
    }
    return render(request, template_name='employee/employee_title.html', context = context)

@login_required
@group_required('Admin', 'HR Admin')
def add_employee_title(request):
    if request.method =='POST':
        form = EmployeeTitleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('employee_title')
    else:
         form = EmployeeTitleForm()
    context = {
        'form': form
    }
    return render(request, template_name='employee/add_employee_title.html', context = context)

@login_required
@group_required('Admin', 'HR Admin')
def update_employee_title(request, pk):
    employee_title = EmployeeTitle.objects.get(id = pk)
    if request.method == 'POST':
        form = EmployeeTitleForm(request.POST, request.FILES, instance = employee_title)
        if form.is_valid():
            form.save()
            return redirect('employee_title')
        else:
            return HttpResponse('Failed to update employee title record.')
    else:
        form = EmployeeTitleForm(instance = employee_title)
    context = {
        'form': form
    }
    return render(request, template_name='employee/add_employee_title.html', context = context)

@login_required
@group_required('Admin', 'HR Admin')
def delete_employee_title(request, pk):
    employee_title = EmployeeTitle.objects.get(id = pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_title')
    context = {
        'employee_title': employee_title
    }
    return render(request, template_name='employee/delete_employee_title.html', context = context)

# Employee Contract views 
@login_required
@group_required('Admin', 'HR Admin')
def employee_contract(request):
    employee_contracts = EmployeeContract.objects.select_related('employee', 'title').all()
    filter_form = EmployeeContractFilterForm(request.GET or None)
    search_form = EmployeeSearchForm(request.GET or None)

    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search')

        # Filter by search query on user's first name and last name
        if search_query:
            employee_contracts = employee_contracts.filter(
               (Q(Q(employee__user__first_name__icontains = search_query) | 
                Q(employee__user__second_name__icontains = search_query)))
            )

  
    if filter_form.is_valid():
        search_query = filter_form.cleaned_data.get('search')
        contract_status = filter_form.cleaned_data['contract_status']
        title = filter_form.cleaned_data.get('job_title')

        # Filter by contract status
        if contract_status == 'active':
            employee_contracts = employee_contracts.filter(contract_status='active')
        elif contract_status == 'inactive':
            employee_contracts = employee_contracts.filter(contract_status='inactive')
        elif contract_status == 'pending':
            employee_contracts = employee_contracts.filter(contract_status='pending')
        else:
            employee_contracts = employee_contracts.all()

        # Filter by job title
        if title:
            employee_contracts = employee_contracts.filter(title=title)

    # employee_contracts = EmployeeContract.objects.all()
    context = {
        # 'employee_contracts': employee_contracts,
        'employee_contracts': employee_contracts,
        'search_form': search_form,
        'filter_form': filter_form,
    }
    return render(request, template_name='employee/employee_contract.html', context = context)

@login_required
@group_required('Admin', 'HR Admin')
def employee_without_contract(request):
    if 'search' in request.GET:
        search_user = request.GET['search']
        employees_without_contract = Employee.objects.filter(Q(Q(employeecontract__isnull =True), Q(employee_firstname__icontains = search_user) | Q(employee_lastname__icontains = search_user)))
    else: 
        employees_without_contract = Employee.objects.filter(employeecontract__isnull =True)
    context = {
        'employees': employees_without_contract,
    }
    return render(request, template_name='employee/new_employee_contract.html', context = context)


@login_required
@group_required('Admin', 'HR Admin')
def add_employee_contract(request, employee_id):
    employee_id = get_object_or_404(Employee, id = employee_id)
    if request.method =='POST':
        form = EmployeeContractForm(request.POST, request.FILES, initial={'employee': employee_id})
        if form.is_valid():
            employee = form.save(commit=False)
            employee.employee = employee_id
            employee.save()
            return redirect('employee')
    else:
         form = EmployeeContractForm(initial={'employee': employee_id,})
    context = {
        'form': form, 
        'user': employee_id
    }

    return render(request, template_name='employee/add_employee_contract.html', context = context)

@login_required
@group_required('Admin', 'HR Admin')
def update_employee_contract(request, pk):
    employee_contract = EmployeeContract.objects.get(id = pk)
    if request.method == 'POST':
        form = EmployeeContractForm(request.POST, request.FILES, instance = employee_contract)
        if form.is_valid():
            form.save()
            return redirect('employee_contract')
        else:
            return HttpResponse('Failed to update employee contract record.')
    else:
        form = EmployeeContractForm(instance = employee_contract)
    context = {
        'form': form
    }
    return render(request, template_name='employee/add_employee_contract.html', context = context)

@login_required
@group_required('Admin', 'HR Admin')
def delete_employee_contract(request, pk):
    employee_contract = EmployeeContract.objects.get(id = pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_contract')
    context = {
        'employee_contract': employee_contract
    }
    return render(request, template_name='employee/delete_employee_contract.html', context = context)
