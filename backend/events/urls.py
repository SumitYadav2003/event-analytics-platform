from django.urls import path
from .views import ingest_event

urlpatterns = [
    path('events/', ingest_event, name='ingest-event'),
]