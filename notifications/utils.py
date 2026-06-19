from .models import Notification


def send_notification(user, type, title, message):
    """Helper to create a notification for a user."""
    Notification.objects.create(
        user    = user,
        type    = type,
        title   = title,
        message = message,
    )