from django.conf import settings
from django.core.mail import send_mail


class EventNotificationService:
    @staticmethod
    def send_registration_email(*, event, user) -> None:
        if not user.email:
            return

        subject = f"Registration confirmed: {event.title}"

        message = (
            f"Hello {user.username},\n\n"
            f"You have successfully registered for the event:\n\n"
            f"Title: {event.title}\n"
            f"Date: {event.starts_at}\n"
            f"Location: {event.location}\n\n"
            f"See you there!"
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
