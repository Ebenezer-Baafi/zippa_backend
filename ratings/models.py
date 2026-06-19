from django.db import models
from accounts.models import User
from jobs.models import DeliveryJob
import uuid


class Rating(models.Model):
    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job        = models.OneToOneField(DeliveryJob, on_delete=models.CASCADE, related_name='rating')
    customer   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_ratings')
    rider      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_ratings')
    score      = models.PositiveSmallIntegerField()  # 1 to 5
    comment    = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating {self.score}⭐ - Job {self.job.id}"