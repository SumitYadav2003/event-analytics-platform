from django.db.models import Sum
from rest_framework.decorators import api_view
from rest_framework.response import Response

from applications.models import Application
from events.models import Event
from .models import AggregatedMetric


def get_application_name(request):
    return request.GET.get('application')


@api_view(['GET'])
def health_check(request):
    return Response({
        "status": "ok",
        "message": "Event Analytics Platform backend is running"
    })


@api_view(['GET'])
def analytics_summary(request):
    application_name = get_application_name(request)
    events = Event.objects.all()

    if application_name:
        events = events.filter(application__name=application_name)

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
    application_name = get_application_name(request)
    metrics = AggregatedMetric.objects.all()

    if application_name:
        metrics = metrics.filter(application__name=application_name)

    data = (
        metrics
        .values('event_type')
        .annotate(count=Sum('count'))
        .order_by('-count')
    )

    return Response({
        "application": application_name,
        "source": "aggregated_metrics",
        "results": list(data)
    })


@api_view(['GET'])
def events_per_day(request):
    application_name = get_application_name(request)
    metrics = AggregatedMetric.objects.all()

    if application_name:
        metrics = metrics.filter(application__name=application_name)

    data = (
        metrics
        .values('date')
        .annotate(count=Sum('count'))
        .order_by('date')
    )

    return Response({
        "application": application_name,
        "source": "aggregated_metrics",
        "results": list(data)
    })