from django.contrib import admin
from .models import RiderProfile

@admin.register(RiderProfile)
class RiderProfileAdmin(admin.ModelAdmin):
    list_display  = ['user', 'vehicle_type', 'is_available', 'is_approved']
    list_editable = ['is_available', 'is_approved']