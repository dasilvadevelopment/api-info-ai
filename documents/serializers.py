import hashlib

from rest_framework import serializers

from .models import Document

CHUNK_SIZE = 1024 * 1024  # stream the file in 1MB chunks


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for documents.

    - ``file`` is write-only: uploads accept a file, but the stored path is
      exposed via the read-only ``file_url`` instead.
    - ``checksum`` is computed server-side from the uploaded file's bytes.
    - ``is_active`` is read-only: it is managed by the supersede logic, never
      set by the client.
    """

    file_url = serializers.SerializerMethodField()
    checksum = serializers.CharField(max_length=64, required=False)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Document
        fields = [
            'id',
            'department',
            'title',
            'file',
            'file_url',
            'checksum',
            'uploaded_by',
            'replaces',
            'is_active',
            'uploaded_at',
        ]
        extra_kwargs = {
            'file': {'write_only': True},
            'department': {'write_only': True},
            'uploaded_by': {'required': False},
            'replaces': {'required': False},
        }

    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.file.url) if request else obj.file.url
        return None

    def create(self, validated_data):
        uploaded_file = validated_data.get('file')
        # Compute the checksum from the uploaded bytes (idempotent: rewind).
        if uploaded_file is not None:
            sha = hashlib.sha256()
            for chunk in uploaded_file.chunks(CHUNK_SIZE):
                sha.update(chunk)
            validated_data['checksum'] = sha.hexdigest()
        else:
            # No file provided (e.g. manual create) -> hash nothing.
            validated_data['checksum'] = hashlib.sha256(b'').hexdigest()
        return super().create(validated_data)
