from rest_framework import serializers
from .models import Negotiation


class NegotiationSerializer(serializers.ModelSerializer):
    sender_name   = serializers.CharField(source='sender.full_name',   read_only=True)
    receiver_name = serializers.CharField(source='receiver.full_name', read_only=True)

    class Meta:
        model  = Negotiation
        fields = [
            'id', 'job', 'sender_name', 'receiver_name',
            'amount', 'status', 'note', 'created_at'
        ]
        read_only_fields = ['id', 'sender_name', 'receiver_name', 'status', 'created_at']


class NegotiationCreateSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    note   = serializers.CharField(required=False, allow_blank=True)


class NegotiationResponseSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=['accepted', 'rejected', 'countered'])
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    note   = serializers.CharField(required=False, allow_blank=True)