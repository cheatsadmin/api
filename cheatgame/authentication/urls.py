from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from cheatgame.authentication.apis import CustomerLoginApi, ManagerLoginApi, AdminLoginApi

urlpatterns = [
        path('jwt/', include(([
            path('customer-login/', CustomerLoginApi.as_view(),name="login"),
            path('manager-login/', ManagerLoginApi.as_view(),name="login"),
            path('admin-login/', AdminLoginApi.as_view(),name="login"),
            path('refresh/', TokenRefreshView.as_view(),name="refresh"),
            path('verify/', TokenVerifyView.as_view(),name="verify"),
            ])), name="jwt"),
]
