from django.contrib import admin
from .models import AggregatedMetric


@admin.register(AggregatedMetric)
class AggregatedMetricAdmin(admin.ModelAdmin):
    list_display = ('application', 'event_type', 'date', 'count', 'unique_users')
    search_fields = ('event_type', 'application__name')
    list_filter = ('application', 'event_type', 'date')