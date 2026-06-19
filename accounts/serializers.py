from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model  = User
        fields = [
            'full_name', 'email', 'phone',
            'password', 'confirm_password', 'role'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."}
            )
        if attrs['role'] not in ['customer', 'rider']:
            raise serializers.ValidationError(
                {"role": "Role must be either 'customer' or 'rider'."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            email      = validated_data['email'],
            password   = validated_data['password'],
            full_name  = validated_data['full_name'],
            phone      = validated_data['phone'],
            role       = validated_data['role'],
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = [
            'id', 'full_name', 'email', 'phone',
            'role', 'profile_photo', 'is_verified', 'created_at'
        ]
        read_only_fields = ['id', 'is_verified', 'created_at']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password]
    )