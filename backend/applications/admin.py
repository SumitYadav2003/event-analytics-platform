from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_key', 'is_active', 'created_at')
    search_fields = ('name', 'api_key')
    list_filter = ('is_active', 'created_at')
    readonly_fields = ('api_key', 'created_at', 'updated_at')