from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Department
from .serializers import DepartmentSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    """CRUD for departments.

    Creating/updating/deleting requires a JWT Bearer token. Listing and
    reading a single department are open so the frontend can offer a
    department picker on the register form.
    """

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return super().get_permissions()


