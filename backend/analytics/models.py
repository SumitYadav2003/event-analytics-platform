from django.db import models
from applications.models import Application


class AggregatedMetric(models.Model):
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='aggregated_metrics'
    )
    event_type = models.CharField(max_length=100)
    date = models.DateField()
    count = models.PositiveIntegerField(default=0)
    unique_users = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('application', 'event_type', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.application.name} - {self.event_type} - {self.date}"