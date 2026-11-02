from django.urls import include, path
from rest_framework import routers

from .views import DepartmentViewSet

router = routers.DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='department')

urlpatterns = [
    path('', include(router.urls)),
]
