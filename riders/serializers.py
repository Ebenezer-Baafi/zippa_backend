from rest_framework import serializers
from .models import RiderProfile


class RiderProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    email     = serializers.CharField(source='user.email',     read_only=True)
    phone     = serializers.CharField(source='user.phone',     read_only=True)
    photo     = serializers.ImageField(source='user.profile_photo', read_only=True)

    class Meta:
        model  = RiderProfile
        fields = [
            'id', 'full_name', 'email', 'phone', 'photo',
            'vehicle_type', 'vehicle_plate', 'license_number',
            'is_available', 'is_approved',
            'current_lat', 'current_lng',
            'rating', 'total_deliveries', 'created_at'
        ]
        read_only_fields = ['id', 'is_approved', 'rating', 'total_deliveries', 'created_at']


class RiderAvailabilitySerializer(serializers.Serializer):
    is_available = serializers.BooleanField(required=True)


class RiderLocationSerializer(serializers.Serializer):
    current_lat = serializers.DecimalField(max_digits=9, decimal_places=6, required=True)
    current_lng = serializers.DecimalField(max_digits=9, decimal_places=6, required=True)