from django.core.management.base import BaseCommand
from analytics.services import aggregate_event_metrics


class Command(BaseCommand):
    help = "Aggregate raw events into AggregatedMetric table"

    def handle(self, *args, **options):
        total = aggregate_event_metrics()
        self.stdout.write(
            self.style.SUCCESS(f"Successfully aggregated {total} metric rows.")
        )