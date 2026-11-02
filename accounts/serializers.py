from rest_framework import serializers
from django.contrib.auth.models import User

from departments.models import Department
from .models import UserAccount


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration (signup).

    `password` is write-only so it is never echoed back in responses.
    `department` is provided by name; it is optional.
    """

    department = serializers.CharField(
        write_only=True, required=False, allow_blank=True, default=''
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'department']
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

    def validate_department(self, value):
        if not value:
            return None
        department = Department.objects.filter(name__iexact=value).first()
        if department is None:
            raise serializers.ValidationError(
                f"Department '{value}' does not exist."
            )
        return department

    def create(self, validated_data):
        department = validated_data.pop('department', None)
        user = User.objects.create_user(**validated_data)
        # Attach the department via the profile (created lazily otherwise).
        UserAccount.objects.create(user=user, department=department)
        return user
