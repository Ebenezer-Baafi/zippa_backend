from rest_framework import serializers
from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    rider_name    = serializers.CharField(source='rider.full_name',    read_only=True)

    class Meta:
        model  = Rating
        fields = [
            'id', 'job', 'customer_name', 'rider_name',
            'score', 'comment', 'created_at'
        ]
        read_only_fields = ['id', 'customer_name', 'rider_name', 'created_at']


class RatingCreateSerializer(serializers.Serializer):
    score   = serializers.IntegerField(min_value=1, max_value=5, required=True)
    comment = serializers.CharField(required=False, allow_blank=True)