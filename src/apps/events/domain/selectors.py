from django.db.models import QuerySet

from apps.events.models import Event, EventRegistration


def get_event_queryset() -> QuerySet[Event]:
    return (
        Event.objects
        .select_related("organizer")
        .all()
    )


def get_event_registrations(*, event: Event) -> QuerySet[EventRegistration]:
    return (
        EventRegistration.objects
        .filter(event=event)
        .select_related("user")
        .order_by("created_at")
    )
