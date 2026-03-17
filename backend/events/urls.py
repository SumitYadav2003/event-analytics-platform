from django.urls import path
from .views import ingest_event, list_events

urlpatterns = [
    path('events/', ingest_event, name='ingest-event'),
    path('events/list/', list_events, name='list-events'),
]