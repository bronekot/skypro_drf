from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CreateCheckoutSessionView,
    CreatePriceView,
    CreateProductView,
    CustomTokenObtainPairView,
    PaymentListView,
    RegisterView,
    UserDetailView,
    UserListView,
)

app_name = "users"

urlpatterns = [
    path("payments/", PaymentListView.as_view(), name="payment-list"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("register/", RegisterView.as_view(), name="register"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("create-product/", CreateProductView.as_view(), name="create-product"),
    path("create-price/", CreatePriceView.as_view(), name="create-price"),
    path(
        "create-checkout-session/",
        CreateCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
]
