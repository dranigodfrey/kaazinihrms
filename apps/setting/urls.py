from django.urls import path
from . import views

urlpatterns = [
    path('', views.setting, name='setting'),
    # holiday urls
    path('holiday', views.holiday, name='holiday'),
    path('add_holiday/', views.add_holiday, name='add_holiday'),
    path('update_holiday/<int:pk>/', views.update_holiday, name='update_holiday'),
    path('delete_holiday/<int:pk>/', views.delete_holiday, name='delete_holiday'),

    # work schedule urls
    path('workschedule', views.workschedule, name='workschedule'),
    path('add_workschedule/', views.add_workschedule, name='add_workschedule'),
    path('update_workschedule/<int:pk>/', views.update_workschedule, name='update_workschedule'),
    path('delete_workschedule/<int:pk>/', views.delete_workschedule, name='delete_workschedule'),


]