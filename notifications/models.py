from django.db import models
from accounts.models import User
import uuid


class Notification(models.Model):
    TYPE_CHOICES = [
        ('job_created',   'Job Created'),
        ('job_accepted',  'Job Accepted'),
        ('job_picked_up', 'Job Picked Up'),
        ('job_delivered', 'Job Delivered'),
        ('job_cancelled', 'Job Cancelled'),
        ('negotiation',   'Negotiation'),
        ('rating',        'Rating Received'),
    ]

    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type       = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title      = models.CharField(max_length=255)
    message    = models.TextField()
    is_read    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.type} - {'Read' if self.is_read else 'Unread'}"