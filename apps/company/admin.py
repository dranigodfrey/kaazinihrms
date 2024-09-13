from django.contrib import admin
from apps.company.models import Company, Department, Office, OfficeDepartment


admin.site.register(Company)
admin.site.register(Department)
admin.site.register(Office)
admin.site.register(OfficeDepartment)
