from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    application = serializers.CharField(source='application.name', read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'application', 'event_type', 'user_id', 'metadata', 'timestamp', 'created_at']
        read_only_fields = ['id', 'application', 'created_at']

    def validate_event_type(self, value):
        if not value.strip():
            raise serializers.ValidationError("Event type cannot be empty.")
        return value

    def validate_user_id(self, value):
        if not value.strip():
            raise serializers.ValidationError("User ID cannot be empty.")
        return value