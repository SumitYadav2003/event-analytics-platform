from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'application', 'user_id', 'timestamp', 'created_at')
    search_fields = ('event_type', 'user_id', 'application__name')
    list_filter = ('event_type', 'application', 'timestamp')