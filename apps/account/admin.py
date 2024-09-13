from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from apps.account.forms import AdminUserCreationForm, CustomUserChangeForm
from django.utils.crypto import get_random_string


User = get_user_model()

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    add_form = AdminUserCreationForm
    form = CustomUserChangeForm

    model = User

    list_display = ('username', 'email', 'first_name','middle_name','second_name','sex', 'is_active',
                    'is_staff', 'is_superuser', 'last_login',)
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'first_name','middle_name','second_name','sex','password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',
         'is_superuser','user_role', 'groups', 'user_permissions')}),
        # ('Dates', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1','password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
