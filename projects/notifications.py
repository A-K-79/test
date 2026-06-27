from .models import Notification


def create_notification(user, message):
    if not user or not getattr(user, "is_authenticated", False):
        return None
    return Notification.objects.create(user=user, message=message)


def notification_context(request):
    if not request.user.is_authenticated:
        return {
            "header_notifications": [],
            "header_notifications_unread_count": 0,
        }

    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
    return {
        "header_notifications": notifications[:5],
        "header_notifications_unread_count": notifications.filter(is_read=False).count(),
    }
