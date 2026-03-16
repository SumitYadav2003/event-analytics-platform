from django.db import models
from applications.models import Application


class Event(models.Model):
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='events'
    )
    event_type = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    metadata = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['event_type']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['user_id']),
        ]

    def __str__(self):
        return f"{self.event_type} - {self.user_id}"