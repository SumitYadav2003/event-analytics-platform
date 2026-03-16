from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['event_type', 'user_id', 'metadata', 'timestamp']

    def validate_event_type(self, value):
        if not value.strip():
            raise serializers.ValidationError("Event type cannot be empty.")
        return value

    def validate_user_id(self, value):
        if not value.strip():
            raise serializers.ValidationError("User ID cannot be empty.")
        return value