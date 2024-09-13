from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification, name='notification'),
    path('update_notification/<int:pk>/', views.update_notification, name='update_notification'),
    path('delete_notification/<int:pk>/', views.delete_notification, name='delete_notification'),
]