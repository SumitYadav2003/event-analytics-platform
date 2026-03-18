from celery import shared_task
from .services import aggregate_event_metrics


@shared_task
def run_aggregate_metrics():
    total = aggregate_event_metrics()
    return f"Successfully aggregated {total} metric rows."