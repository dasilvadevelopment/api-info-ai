from django.conf import settings
from django.db import models


class UserAccount(models.Model):
    """Extra profile data for a User, including their department.

    Kept separate from django.contrib.auth.models.User so the built-in
    auth model stays untouched. Access it via ``user.useraccount``.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='useraccount',
    )
    department = models.ForeignKey(
        'departments.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='members',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'UserAccount({self.user.username})'

