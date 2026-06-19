from django.contrib import admin
from .models import DeliveryJob

@admin.register(DeliveryJob)
class DeliveryJobAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'rider', 'package_type', 'status', 'created_at']
    list_filter  = ['status', 'package_type']