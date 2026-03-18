from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .throttles import EventIngestionRateThrottle
from rest_framework.decorators import api_view, throttle_classes

from applications.models import Application
from .models import Event
from .serializers import EventSerializer


def get_application_from_api_key(request):
    api_key = request.headers.get('X-API-KEY')

    if not api_key:
        return None, Response(
            {"error": "Missing X-API-KEY header."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        application = Application.objects.get(api_key=api_key, is_active=True)
        return application, None
    except Application.DoesNotExist:
        return None, Response(
            {"error": "Invalid or inactive API key."},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@throttle_classes([EventIngestionRateThrottle])
def ingest_event(request):
    application, error_response = get_application_from_api_key(request)
    if error_response:
        return error_response

    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(application=application)
        return Response(
            {
                "message": "Event ingested successfully.",
                "application": application.name,
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_events(request):
    events = Event.objects.select_related('application').all()

    application_name = request.GET.get('application')
    event_type = request.GET.get('event_type')
    user_id = request.GET.get('user_id')

    if application_name:
        events = events.filter(application__name=application_name)

    if event_type:
        events = events.filter(event_type=event_type)

    if user_id:
        events = events.filter(user_id=user_id)

    paginator = Paginator(events, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    serializer = EventSerializer(page_obj.object_list, many=True)

    return Response({
        "count": paginator.count,
        "total_pages": paginator.num_pages,
        "current_page": page_obj.number,
        "next_page": page_obj.next_page_number() if page_obj.has_next() else None,
        "previous_page": page_obj.previous_page_number() if page_obj.has_previous() else None,
        "results": serializer.data
    })