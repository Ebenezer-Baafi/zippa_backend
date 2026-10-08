from rest_framework import serializers
from .models import DeliveryJob


class DeliveryJobSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    rider_name    = serializers.CharField(source='rider.user.full_name', read_only=True)
    has_rated     = serializers.SerializerMethodField()

    class Meta:
        model  = DeliveryJob
        fields = [
            'id', 'customer_name', 'rider_name',
            'package_type', 'package_description',
            'pickup_address', 'pickup_lat', 'pickup_lng',
            'dropoff_address', 'dropoff_lat', 'dropoff_lng',
            'estimated_fare', 'final_fare',
            'status',
            'has_rated',
            'created_at', 'accepted_at', 'picked_up_at', 'delivered_at',
        ]
        read_only_fields = [
            'id', 'customer_name', 'rider_name', 'status',
            'final_fare', 'has_rated',
            'created_at', 'accepted_at', 'picked_up_at', 'delivered_at',
        ]

    def get_has_rated(self, obj):
        # A job has at most one Rating (OneToOneField), so .exists() is fine.
        return hasattr(obj, 'rating')


class JobStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=['accepted', 'picked_up', 'delivered', 'cancelled']
    )