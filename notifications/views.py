from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework             import status
from rest_framework.permissions import IsAuthenticated

from .models        import Notification
from .serializers   import NotificationSerializer


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get all notifications for the logged in user."""
        notifications = Notification.objects.filter(
            user=request.user
        ).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NotificationReadView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, notification_id):
        """Mark a single notification as read."""
        try:
            notification = Notification.objects.get(
                id=notification_id, user=request.user
            )
            notification.is_read = True
            notification.save()
            return Response(
                {'detail': 'Notification marked as read.'},
                status=status.HTTP_200_OK
            )
        except Notification.DoesNotExist:
            return Response(
                {'detail': 'Notification not found.'},
                status=status.HTTP_404_NOT_FOUND
            )


class NotificationReadAllView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        """Mark all notifications as read."""
        Notification.objects.filter(
            user=request.user, is_read=False
        ).update(is_read=True)
        return Response(
            {'detail': 'All notifications marked as read.'},
            status=status.HTTP_200_OK
        )


class UnreadCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get count of unread notifications."""
        count = Notification.objects.filter(
            user=request.user, is_read=False
        ).count()
        return Response({'unread_count': count}, status=status.HTTP_200_OK)