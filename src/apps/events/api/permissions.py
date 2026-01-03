from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOrganizerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.organizer == request.user


class IsEventOrganizer(BasePermission):
    """
    Access only for event organizer.
    """

    def has_object_permission(self, request, view, obj):
        return obj.organizer == request.user
