from django.db import models


class Department(models.Model):
    """A department that accounts can be assigned to."""

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'departments'

    def __str__(self):
        return self.name

