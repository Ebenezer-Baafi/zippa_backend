from django.urls import path
from .views import NotificationListView, NotificationReadView, NotificationReadAllView, UnreadCountView

urlpatterns = [
    path('',                            NotificationListView.as_view(),   name='notification-list'),
    path('unread/',                     UnreadCountView.as_view(),        name='unread-count'),
    path('read-all/',                   NotificationReadAllView.as_view(), name='read-all'),
    path('<uuid:notification_id>/read/', NotificationReadView.as_view(),  name='notification-read'),
]