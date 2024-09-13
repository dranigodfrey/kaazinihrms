from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from django.contrib.auth import get_user_model

User = get_user_model()

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'middle_name', 'second_name', 'sex', 'user_role', 'is_active', 'is_staff', ' is_superuser', 'last_login', 'date_joined')
        export_order = ('id', 'username', 'first_name', 'middle_name', 'second_name', 'sex', 'user_role', 'is_active', 'is_staff', ' is_superuser', 'last_login', 'date_joined')
