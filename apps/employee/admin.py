from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.employee.models import Employee, EmployeeTitle, EmployeeContract

admin.site.register(Employee)
admin.site.register(EmployeeContract)
admin.site.register(EmployeeTitle)