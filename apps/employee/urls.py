from django.urls import path
from . import views


urlpatterns = [
    # employee urls
    path('', views.employee, name='employee'),
    path('employee_profile', views.employee_profile, name='employee_profile'),
    path('user_list/', views.user_list, name='user_list'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('update_employee/<int:pk>/', views.update_employee, name='update_employee'),
    path('delete_employee/<int:pk>/', views.delete_employee, name='delete_employee'),
    path('export-employees/', views.export_employees_to_excel, name='export-employees'),
    path('export-employee-contract/', views.export_employee_contract_to_excel, name='export-employee-contract'),
    
    # employee titles urls
    path('employee_title', views.employee_title, name='employee_title'),
    path('add_employee_title/', views.add_employee_title, name='add_employee_title'),
    path('update_employee_title/<int:pk>/', views.update_employee_title, name='update_employee_title'),
    path('delete_employee_title/<int:pk>/', views.delete_employee_title, name='delete_employee_title'),

    # employee contracts urls
    path('employee_contract', views.employee_contract, name='employee_contract'),
    path('employee_without_contract', views.employee_without_contract, name='employee_without_contract'),
    path('add_employee_contract/<int:employee_id>/', views.add_employee_contract, name='add_employee_contract'),
    path('update_employee_contract/<int:pk>/', views.update_employee_contract, name='update_employee_contract'),
    path('delete_employee_contract/<int:pk>/', views.delete_employee_contract, name='delete_employee_contract'),

    # employee department manager urls
    # path('department_manager', views.department_manager, name='department_manager'),
    # path('add_department_manager/', views.add_department_manager, name='add_department_manager'),
    # path('update_department_manager/<int:pk>/', views.update_department_manager, name='update_department_manager'),
    # path('delete_department_manager/<int:pk>/', views.delete_department_manager, name='delete_department_manager'),
]