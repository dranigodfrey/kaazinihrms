from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from apps.tenant.models import Client,Domain

class DomainInline(admin.TabularInline):
        model = Domain
        max_mum = 1


@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
        list_display = ('name', 'schema_name')
        inlines = [DomainInline]