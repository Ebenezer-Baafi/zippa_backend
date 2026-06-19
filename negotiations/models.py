from django.db import models
from accounts.models import User
from jobs.models import DeliveryJob
import uuid


class Negotiation(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('accepted',  'Accepted'),
        ('rejected',  'Rejected'),
        ('countered', 'Countered'),
    ]

    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job         = models.ForeignKey(DeliveryJob, on_delete=models.CASCADE, related_name='negotiations')
    sender      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_negotiations')
    receiver    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_negotiations')
    amount      = models.DecimalField(max_digits=10, decimal_places=2)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    note        = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Negotiation {self.id} - Job {self.job.id} [{self.status}]"