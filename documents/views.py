from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db import transaction
from django.http import FileResponse

from .models import Document
from .serializers import DocumentSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    """CRUD for department documents.

    All actions require a JWT Bearer token. On create, if an *active* document
    with the same checksum already exists in the same department, the new
    document supersedes it (``replaces`` is set and the old one is marked
    inactive) instead of creating a stray duplicate.
    """

    queryset = Document.objects.all().select_related('department', 'uploaded_by')
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        document = serializer.save(uploaded_by=request.user)

        # Supersede an existing active duplicate (same content, same department).
        # Order by pk so the oldest version is always the one superseded
        # (uploaded_at has second-level precision and can tie).
        previous = (
            Document.objects.filter(
                department=document.department,
                checksum=document.checksum,
                is_active=True,
            )
            .exclude(pk=document.pk)
            .order_by('pk')
            .first()
        )
        if previous is not None:
            document.replaces = previous
            document.save(update_fields=['replaces'])
            previous.is_active = False
            previous.save(update_fields=['is_active'])

        return Response(self.get_serializer(document).data, status=201)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Stream the document file (auth-gated)."""
        document = self.get_object()
        try:
            document.file.open('rb')
        except FileNotFoundError:
            return Response({'detail': 'File not found on disk.'}, status=404)
        filename = document.file.name.rsplit('/', 1)[-1] or 'download'
        return FileResponse(
            document.file,
            as_attachment=True,
            filename=filename,
            content_type='application/octet-stream',
        )

