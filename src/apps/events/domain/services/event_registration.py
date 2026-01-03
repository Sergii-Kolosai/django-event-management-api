from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone

from apps.events.models import EventRegistration
from apps.events.domain.services.notifications import EventNotificationService


class EventRegistrationService:
    @staticmethod
    def register_user(*, event, user) -> EventRegistration:
        if event.starts_at < timezone.now():
            raise ValidationError("You cannot register for a past event.")

        try:
            registration = EventRegistration.objects.create(
                event=event,
                user=user,
            )
        except IntegrityError:
            raise ValidationError("You are already registered for this event.")

        EventNotificationService.send_registration_email(
            event=event,
            user=user,
        )

        return registration
