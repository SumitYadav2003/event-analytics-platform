from django.db.models import Count
from django.db.models.functions import TruncDate

from events.models import Event
from .models import AggregatedMetric


def aggregate_event_metrics():
    aggregated_data = (
        Event.objects
        .annotate(day=TruncDate('timestamp'))
        .values('application', 'event_type', 'day')
        .annotate(
            count=Count('id'),
            unique_users=Count('user_id', distinct=True)
        )
        .order_by('application', 'event_type', 'day')
    )

    created_or_updated = 0

    for item in aggregated_data:
        AggregatedMetric.objects.update_or_create(
            application_id=item['application'],
            event_type=item['event_type'],
            date=item['day'],
            defaults={
                'count': item['count'],
                'unique_users': item['unique_users']
            }
        )
        created_or_updated += 1

    return created_or_updated