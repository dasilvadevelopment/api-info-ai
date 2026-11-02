from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration (signup).

    `password` is write-only so it is never echoed back in responses.
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': False},
        }

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                'A user with that username already exists.'
            )
        return value

    def create(self, validated_data):
        # create_user() hashes the password via the configured hasher.
        return User.objects.create_user(**validated_data)
