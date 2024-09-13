from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.leave_dashboard, name='leave_dashboard'),
    path('get_leave_data/', views.get_leave_data, name='get_leave_data'),
    path('leave_type/', views.leave_type, name='leave_type'),
    path('add_leave_type/', views.add_leave_type, name='add_leave_type'),
    path('update_leave_type/<int:pk>/', views.update_leave_type, name='update_leave_type'),
    path('delete_leave_type/<int:pk>/', views.delete_leave_type, name='delete_leave_type'),

    # Employee leave urls
    path('employee_leave/', views.employee_leave, name='employee_leave'),
    path('add_employee_leave/', views.add_employee_leave, name='add_employee_leave'),
    path('update_employee_leave/<int:pk>/', views.update_employee_leave, name='update_employee_leave'),
    path('delete_employee_leave/<int:pk>/', views.delete_employee_leave, name='delete_employee_leave'),

    # Employee leave request urls
    path('leave_request/', views.leave_request, name='leave_request'),
    path('approve_leave/', views.approve_leave, name='approve_leave'),
    path('add_leave_request/', views.add_leave_request, name='add_leave_request'),
    path('update_leave_request/<int:pk>/', views.update_leave_request, name='update_leave_request'),
    path('delete_leave_request/<int:pk>/', views.delete_leave_request, name='delete_leave_request'),

    # Employee leave approval urls
     path('update_leave_approval/<int:pk>/', views.update_leave_approval, name='update_leave_approval'),

    path('pending_leave/', views.employee_leave_pending, name='pending_leave'),
    path('approved_leave/', views.employee_leave_approved, name='approved_leave'),
    path('rejected_leave/', views.employee_leave_rejected, name='rejected_leave'),

    path('export_leave/', views.export_leaves_to_excel, name='export_leave'),
    
]