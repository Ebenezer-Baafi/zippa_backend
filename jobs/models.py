from django.db import models
from accounts.models import User
from riders.models import RiderProfile
import uuid


class DeliveryJob(models.Model):
    STATUS_CHOICES = [
        ('pending',    'Pending'),
        ('accepted',   'Accepted'),
        ('picked_up',  'Picked Up'),
        ('delivered',  'Delivered'),
        ('cancelled',  'Cancelled'),
    ]

    PACKAGE_CHOICES = [
        ('document',   'Document'),
        ('small',      'Small Package'),
        ('medium',     'Medium Package'),
        ('large',      'Large Package'),
        ('fragile',    'Fragile'),
    ]

    id                  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer            = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    rider               = models.ForeignKey(RiderProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='jobs')
    
    # Package info
    package_type        = models.CharField(max_length=20, choices=PACKAGE_CHOICES)
    package_description = models.TextField(blank=True)
    
    # Pickup
    pickup_address      = models.TextField()
    pickup_lat          = models.DecimalField(max_digits=9, decimal_places=6)
    pickup_lng          = models.DecimalField(max_digits=9, decimal_places=6)
    
    # Dropoff
    dropoff_address     = models.TextField()
    dropoff_lat         = models.DecimalField(max_digits=9, decimal_places=6)
    dropoff_lng         = models.DecimalField(max_digits=9, decimal_places=6)
    
    # Pricing
    estimated_fare      = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    final_fare          = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Status
    status              = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Timestamps
    created_at          = models.DateTimeField(auto_now_add=True)
    accepted_at         = models.DateTimeField(null=True, blank=True)
    picked_up_at        = models.DateTimeField(null=True, blank=True)
    delivered_at        = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Job {self.id} - {self.customer.full_name} [{self.status}]"