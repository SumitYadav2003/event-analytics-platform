from django.urls import path
from .views import health_check, analytics_summary, events_by_type, events_per_day

urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('analytics/summary/', analytics_summary, name='analytics-summary'),
    path('analytics/by-type/', events_by_type, name='events-by-type'),
    path('analytics/per-day/', events_per_day, name='events-per-day'),
]