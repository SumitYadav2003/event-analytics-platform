from django.db.models import Count
from django.db.models.functions import TruncDate
from rest_framework.decorators import api_view
from rest_framework.response import Response

from applications.models import Application
from events.models import Event


@api_view(['GET'])
def health_check(request):
    return Response({
        "status": "ok",
        "message": "Event Analytics Platform backend is running"
    })


@api_view(['GET'])
def analytics_summary(request):
    total_events = Event.objects.count()
    total_unique_users = Event.objects.values('user_id').distinct().count()
    total_applications = Application.objects.count()

    return Response({
        "total_events": total_events,
        "total_unique_users": total_unique_users,
        "total_applications": total_applications
    })


@api_view(['GET'])
def events_by_type(request):
    data = (
        Event.objects
        .values('event_type')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    return Response(list(data))


@api_view(['GET'])
def events_per_day(request):
    data = (
        Event.objects
        .annotate(day=TruncDate('timestamp'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    return Response(list(data))