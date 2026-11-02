from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterView

urlpatterns = [
    # POST /api/auth/login/    -> {"username", "password"} => {"access", "refresh"}
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # POST /api/auth/refresh/  -> {"refresh"} => {"access"}
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # POST /api/auth/register/ -> create account
    path('register/', RegisterView.as_view(), name='register'),
]
