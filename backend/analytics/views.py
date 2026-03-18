from django.db.models import Count
from django.db.models.functions import TruncDate
from rest_framework.decorators import api_view
from rest_framework.response import Response

from applications.models import Application
from events.models import Event


def filter_events_by_application(request):
    application_name = request.GET.get('application')
    events = Event.objects.all()

    if application_name:
        events = events.filter(application__name=application_name)

    return events, application_name


@api_view(['GET'])
def health_check(request):
    return Response({
        "status": "ok",
        "message": "Event Analytics Platform backend is running"
    })


@api_view(['GET'])
def analytics_summary(request):
    events, application_name = filter_events_by_application(request)

    total_events = events.count()
    total_unique_users = events.values('user_id').distinct().count()

    if application_name:
        total_applications = 1 if Application.objects.filter(name=application_name).exists() else 0
    else:
        total_applications = Application.objects.count()

    return Response({
        "application": application_name,
        "total_events": total_events,
        "total_unique_users": total_unique_users,
        "total_applications": total_applications
    })


@api_view(['GET'])
def events_by_type(request):
    events, application_name = filter_events_by_application(request)

    data = (
        events
        .values('event_type')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    return Response({
        "application": application_name,
        "results": list(data)
    })


@api_view(['GET'])
def events_per_day(request):
    events, application_name = filter_events_by_application(request)

    data = (
        events
        .annotate(day=TruncDate('timestamp'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    return Response({
        "application": application_name,
        "results": list(data)
    })