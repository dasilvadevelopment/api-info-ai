from rest_framework import serializers

from .models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department (used for list/create and read-only display)."""

    class Meta:
        model = Department
        fields = ['id', 'name', 'description']
        extra_kwargs = {
            'description': {'required': False},
        }
