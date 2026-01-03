from django.contrib import admin

from .models import Event, EventRegistration


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "starts_at",
        "location",
        "organizer",
        "created_at",
    )
    list_filter = ("starts_at", "location")
    search_fields = ("title", "description", "location")
    ordering = ("starts_at",)


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "event",
        "user",
        "created_at",
    )
    list_filter = ("event", "created_at")
    search_fields = (
        "event__title",
        "user__username",
    )
