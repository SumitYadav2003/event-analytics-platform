from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from applications.models import Application
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