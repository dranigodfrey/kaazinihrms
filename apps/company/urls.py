from django.urls import path
from . import views

urlpatterns = [
    # company urls
    path('comapny', views.company, name='company'),
    path('', views.main_dashboard, name='main_dashboard'),
    path('add_company/', views.add_company, name='add_company'),
    path('update_company/<int:pk>/', views.update_company, name='update_company'),
    path('delete_company/<int:pk>/', views.delete_company, name='delete_company'),
    # office urls
    path('office', views.office, name='office'),
    path('add_office/', views.add_office, name='add_office'),
    path('update_office/<int:pk>/', views.update_office, name='update_office'),
    path('delete_office/<int:pk>/', views.delete_office, name='delete_office'),
    # department urls
    path('department', views.department, name='department'),
    path('add_department/', views.add_department, name='add_department'),
    path('update_department/<int:pk>/', views.update_department, name='update_department'),
    path('delete_department/<int:pk>/', views.delete_department, name='delete_department'),

    # office department urls
    path('office_department', views.office_department, name='office_department'),
    path('assign_department/', views.assign_office_department, name='assign_office_department'),
    path('update_office_department/<int:pk>/', views.update_office_department, name='update_office_department'),

    path('gender-chart/', views.employee_gender_chart, name='employee_gender_chart'),
    path('api/gender-data/', views.employee_gender_data, name='employee_gender_data'),

    path('employee-title-data/', views.employee_title_data, name='employee_title_data'),
    path('employee-department-data/', views.employee_department_data, name='employee_department_data'),
]