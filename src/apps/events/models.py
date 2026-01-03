from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    starts_at = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="organized_events",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("starts_at",)
        indexes = [
            models.Index(fields=["organizer"]),
            models.Index(fields=["starts_at"]),
            models.Index(fields=["location"]),
        ]

    def __str__(self) -> str:
        return f"{self.title} @ {self.starts_at}"


class EventRegistration(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="registrations",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="event_registrations",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("event", "user"),
                name="unique_event_user_registration",
            )
        ]
        indexes = [
            models.Index(fields=["event"]),
            models.Index(fields=["user"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.user} -> {self.event}"
