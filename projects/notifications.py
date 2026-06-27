from .models import Notification


def create_notification(user, message):
    if not user or not getattr(user, "is_authenticated", False):
        return None
    return Notification.objects.create(user=user, message=message)


def create_notifications_for_users(users, message, exclude_user_ids=None):
    exclude_user_ids = set(exclude_user_ids or [])
    sent_user_ids = set()
    created_notifications = []

    for user in users:
        if not user:
            continue
        if user.id in exclude_user_ids or user.id in sent_user_ids:
            continue
        notification = create_notification(user, message)
        if notification:
            created_notifications.append(notification)
            sent_user_ids.add(user.id)

    return created_notifications


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
