from django.conf import settings
from django.db import models
from django.urls import reverse


class Document(models.Model):
    """A file owned by a department, with versioning and duplicate tracking.

    - ``checksum`` is the SHA-256 of the file bytes, used to detect exact
      duplicates (same content uploaded again).
    - ``replaces`` points at the previous version of this document; the old
      version is marked ``is_active=False`` when it is superseded.
    - ``is_active`` is False when a document has been superseded or removed.
    """

    department = models.ForeignKey(
        'departments.Department', on_delete=models.PROTECT, related_name='documents'
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    checksum = models.CharField(max_length=64)          # detect exact duplicates
    replaces = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='replaced_by'
    )
    is_active = models.BooleanField(default=True)       # False when superseded or removed
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        indexes = [models.Index(fields=['department', 'checksum'])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('document-download', kwargs={'pk': self.pk})

