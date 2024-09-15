from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    PaymentListView,
    UserListView,
    UserDetailView,
    RegisterView,
    CustomTokenObtainPairView,
)

app_name = "users"

urlpatterns = [
    path("payments/", PaymentListView.as_view(), name="payment-list"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("register/", RegisterView.as_view(), name="register"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
