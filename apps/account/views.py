from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.urls import reverse
from .forms import CustomUserCreationForm, UserGroupForm,EditUserForm
from django.contrib import messages
from django.db.models import Q
from .resources import UserResource
from apps.account.decorators import group_required
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from premailer import transform
from django.utils.html import strip_tags
from django.template.loader import render_to_string



User = get_user_model()


@login_required
def dashboard(request):
    active_user = request.user

    for group in Group.objects.all():
        if active_user.groups.filter(name='Admin').exists():
                 return render(request, template_name='company/main_dashboard.html')
            # elif active_user.groups.filter(name='HR Admin').exists():
            #     return render(request, 'dashboards/hr_dashboard.html')
            # elif active_user.groups.filter(name='Manager').exists():
            #     return render(request, 'dashboards/manager_dashboard.html')
            # elif active_user.groups.filter(name='Supervisor').exists():
            #     return render(request, 'dashboards/supervisor_dashboard.html')
            # elif active_user.groups.filter(name='Employee').exists():
            #     return render(request, 'dashboards/employee_dashboard.html')
        else:
            return render(request, template_name='company/main_dashboard.html')

# Export Users 
@login_required
@group_required('Admin', 'HR Admin')
def export_users_to_excel(request):
    employee_resource = UserResource()
    dataset = employee_resource.export()
    response = HttpResponse(dataset.export('xlsx'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="users.xlsx"'
    return response

# def dashboard(request):
#     users = User.objects.all()
#     admins = ['admin','executive','hr manager']
#     context = {
#         'users':users,
#         'admins': admins,
#     }
#     return render(request, template_name='dashboard.html', context=context)

@login_required
@group_required('Admin')
def account(request):
    if request.user.is_superuser and 'search' in request.GET:
        search_user = request.GET['search']
        users = User.objects.filter(Q(Q(username__icontains = search_user) | Q(email__icontains = search_user) | Q(user_role__icontains = search_user) ))
    else:
        users = User.objects.all()
    context = {
        'users':users,
    }
    return render(request, template_name='account/index.html', context=context)
@login_required
@group_required('Admin')
def sign_up(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user, password = form.save()
            
            # Generate one-time use token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Create password reset link
            reset_url = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )
             # Render email template
            email_template = render_to_string('account/user_creation_email.html', {
                'user': user,
                'reset_url': reset_url,
                'username': user.username,
                'password': password,
            })

            # Transform CSS to inline styles
            html_message = transform(email_template)
            plain_message = strip_tags(html_message)
            # Send email
            send_mail(
                'Welcome to Kaazini HRMS',
                plain_message,
                'systems@kaazini.com',
                [user.email],
                fail_silently=False,
                html_message=html_message
            )
            return redirect('account')
        else:
             messages.error(request, 'Failed to save record please check your inputs!')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, template_name='account/sign_up.html', context=context)

def sign_in(request):
    if request.method =="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('leave_dashboard')
        else:
             messages.error(request, 'Access denied please check your email and password.')
    return render(request, template_name='account/login.html')

@login_required

def change_user_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Successfully updated user info')
            return redirect('account')  # Redirect to a user detail or success page
    else:
        form = EditUserForm(instance=user)
    
    return render(request, 'account/change_user.html', {'form': form, 'user': user})

@login_required
def logout_user(request):
    logout(request)
    return redirect('login')


def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Admin').exists()

# @login_required
# @user_passes_test(is_admin)
# def role_list(request):
#     roles = Group.objects.all()
#     return render(request, 'account/role_list.html', {'roles': roles})

@login_required
@user_passes_test(is_admin)
def role_create(request):
    roles = Group.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        group, created = Group.objects.get_or_create(name=name)
        if created:
            return redirect('role_create')
    context = {
        'roles': roles
    }
    return render(request, 'account/role_list.html',context=context)

@login_required
@user_passes_test(is_admin)
def role_edit(request, role_id):
    role = get_object_or_404(Group, id=role_id)
    all_permissions = Permission.objects.all()
    if request.method == 'POST':
        selected_permissions = request.POST.getlist('permissions')
        role.permissions.set(selected_permissions)
        messages.success(request, 'Form submitted successfully!')
        return redirect('role_create')
    return render(request, 'account/role_edit.html', {'role': role, 'permissions': all_permissions})

@login_required
@user_passes_test(is_admin)
def role_delete(request, role_id):
    role = get_object_or_404(Group, id=role_id)
    if request.method == 'POST':
        role.delete()
        return redirect('role_create')
    return render(request, 'account/role_delete.html', {'role': role})


@login_required
def assign_user_to_group(request):
    if request.method == 'POST':
        form = UserGroupForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            groups = form.cleaned_data['groups']
            user.groups.set(groups)  # Set the groups directly, removing old ones
            user.save()
            return redirect('success_page')  # Redirect to a success page or wherever you want
    else:
        form = UserGroupForm()
    
    return render(request, 'account/assign_user_to_group.html', {'form': form})
