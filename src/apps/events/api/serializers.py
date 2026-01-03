from django.contrib.auth.models import User
from rest_framework import serializers

from apps.events.models import Event, EventRegistration


class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class EventListSerializer(serializers.ModelSerializer):
    organizer = OrganizerSerializer(read_only=True)

    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "starts_at",
            "location",
            "organizer",
        )


class EventDetailSerializer(serializers.ModelSerializer):
    organizer = OrganizerSerializer(read_only=True)

    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "description",
            "starts_at",
            "location",
            "organizer",
            "created_at",
            "updated_at",
        )


class EventCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "title",
            "description",
            "starts_at",
            "location",
        )


class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = (
            "id",
            "event",
            "user",
            "created_at",
        )
        read_only_fields = fields


class EventRegistrationListSerializer(serializers.ModelSerializer):
    user = OrganizerSerializer(read_only=True)

    class Meta:
        model = EventRegistration
        fields = (
            "id",
            "user",
            "created_at",
        )
