from django.urls import path
from . import views


urlpatterns = [
    path('', views.account, name='account'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('login', views.sign_in, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('export-users/', views.export_users_to_excel, name='export-users'),
    # path('roles/', views.role_list, name='role_list'),
    path('roles/', views.role_create, name='role_create'),
    path('roles/edit/<int:role_id>/', views.role_edit, name='role_edit'),
    path('roles/delete/<int:role_id>/', views.role_delete, name='role_delete'),
    path('assign-user-to-group/', views.assign_user_to_group, name='assign_user_to_group'),
     path('user/<int:user_id>/edit/', views.change_user_view, name='change_user'),
]