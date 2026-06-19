from django.db import models
from accounts.models import User
import uuid

class RiderProfile(models.Model):
    VEHICLE_CHOICES = [
        ('bicycle',    'Bicycle'),
        ('motorcycle', 'Motorcycle'),
        ('car',        'Car'),
        ('van',        'Van'),
    ]

    id               = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user             = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rider_profile')
    vehicle_type     = models.CharField(max_length=20, choices=VEHICLE_CHOICES)
    vehicle_plate    = models.CharField(max_length=20)
    license_number   = models.CharField(max_length=50)
    is_available     = models.BooleanField(default=False)
    is_approved      = models.BooleanField(default=False)  # admin approves riders
    current_lat      = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    current_lng      = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    rating           = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_deliveries = models.IntegerField(default=0)
    created_at       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.vehicle_type}"