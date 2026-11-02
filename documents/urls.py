from django.urls import include, path
from rest_framework import routers

from .views import DocumentViewSet

router = routers.DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='document')

urlpatterns = [
    path('', include(router.urls)),
    # Named route used by Document.get_absolute_url() and the download action.
    path('documents/<int:pk>/download/', DocumentViewSet.as_view({'get': 'download'}), name='document-download'),
]
