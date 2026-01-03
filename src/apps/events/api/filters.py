import django_filters

from ..models import Event


class EventFilter(django_filters.FilterSet):
    starts_at__gte = django_filters.DateTimeFilter(
        field_name="starts_at",
        lookup_expr="gte",
    )
    starts_at__lte = django_filters.DateTimeFilter(
        field_name="starts_at",
        lookup_expr="lte",
    )
    location = django_filters.CharFilter(
        field_name="location",
        lookup_expr="icontains",
    )

    class Meta:
        model = Event
        fields = (
            "starts_at__gte",
            "starts_at__lte",
            "location",
            "organizer",
        )
