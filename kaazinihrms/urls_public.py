from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
 
    # class based generic views - routes 
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = 'account/reset_password.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = 'account/reset_password_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name ='account/reset.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'account/reset_password_complete.html'), name='password_reset_complete'),
    path('change_password/', auth_views.PasswordChangeView.as_view(template_name = 'account/password_change.html'),  name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name = 'account/password_change_done.html'),  name='password_change_done'),

    # install apps routes
    path('account/', include('apps.account.urls')),
    path('', include('apps.company.urls')),
    path('employee/', include('apps.employee.urls')),
    path('leave/', include('apps.leave.urls')),
    path('setting/', include('apps.setting.urls')),
    path('notification/', include('apps.notification.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
