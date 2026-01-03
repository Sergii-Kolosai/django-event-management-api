from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from apps.events.domain.selectors import get_event_queryset, get_event_registrations
from apps.events.domain.services import EventRegistrationService
from .filters import EventFilter
from .permissions import IsOrganizerOrReadOnly, IsEventOrganizer
from .serializers import (
    EventListSerializer,
    EventDetailSerializer,
    EventCreateUpdateSerializer,
    EventRegistrationSerializer,
    EventRegistrationListSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="List events",
        description="Public endpoint. Returns a list of events with filtering, search and ordering.",
        parameters=[
            OpenApiParameter(
                name="search",
                description="Search by event title or description",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="location",
                description="Filter events by location",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="starts_at__gte",
                description="Filter events starting after the given date",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="ordering",
                description="Ordering by fields, e.g. starts_at or -starts_at",
                required=False,
                type=str,
            ),
        ],
    ),
    retrieve=extend_schema(
        summary="Retrieve event details",
        description="Public endpoint. Returns detailed information about a specific event.",
    ),
    create=extend_schema(
        summary="Create event",
        description="Create a new event. Authentication required.",
    ),
    update=extend_schema(
        summary="Replace event",
        description="Fully update an event. Only the event organizer is allowed to update.",
    ),
    partial_update=extend_schema(
        summary="Update event",
        description="Update an existing event. Only the event organizer is allowed to update.",
    ),
    destroy=extend_schema(
        summary="Delete event",
        description="Delete an event. Only the event organizer is allowed to delete.",
    ),

)
class EventViewSet(viewsets.ModelViewSet):
    queryset = get_event_queryset()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOrganizerOrReadOnly,
    ]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
    ]
    filterset_class = EventFilter
    search_fields = (
        "title",
        "description",
    )
    ordering_fields = ("starts_at", "created_at")
    ordering = ("starts_at",)

    def get_serializer_class(self):
        if self.action == "list":
            return EventListSerializer
        if self.action == "retrieve":
            return EventDetailSerializer
        if self.action == "register":
            return EventRegistrationSerializer
        if self.action == "registrations":
            return EventRegistrationListSerializer
        return EventCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @extend_schema(
        summary="Register for event",
        description="Register the authenticated user for the selected event.",
        responses={201: EventRegistrationSerializer},
    )
    @action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def register(self, request, pk=None):
        event = self.get_object()
        registration = EventRegistrationService.register_user(
            event=event,
            user=request.user,
        )
        serializer = self.get_serializer(registration)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="List event registrations",
        description="Returns a list of users registered for the event. Only available to the event organizer.",
    )
    @action(
        detail=True,
        methods=["get"],
        permission_classes=[permissions.IsAuthenticated, IsEventOrganizer],
    )
    def registrations(self, request, pk=None):
        event = self.get_object()
        queryset = get_event_registrations(event=event)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
