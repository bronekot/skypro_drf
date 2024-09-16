import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .filters import PaymentFilter
from .models import Course, Lesson, Payment
from .permissions import IsModerator, IsOwner
from .serializers import (CourseSerializer, CustomTokenObtainPairSerializer,
                          LessonSerializer, PaymentSerializer,
                          RegisterSerializer, UserSerializer)


@extend_schema(tags=["Payments"])
class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter


User = get_user_model()


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = [permissions.IsAuthenticated, IsOwner]
        elif self.action in ["destroy"]:
            self.permission_classes = [permissions.IsAuthenticated, IsModerator]
        else:
            self.permission_classes = [
                permissions.IsAuthenticated,
                IsModerator | IsOwner,
            ]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = [permissions.IsAuthenticated, IsOwner]
        elif self.action in ["destroy"]:
            self.permission_classes = [permissions.IsAuthenticated, IsModerator]
        else:
            self.permission_classes = [
                permissions.IsAuthenticated,
                IsModerator | IsOwner,
            ]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CreateProductView(APIView):
    def post(self, request):
        try:
            product = stripe.Product.create(
                name=request.data["name"],
                description=request.data.get("description", ""),
            )
            return Response(product, status=status.HTTP_201_CREATED)
        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CreatePriceView(APIView):
    def post(self, request):
        try:
            price = stripe.Price.create(
                product=request.data["product_id"],
                unit_amount=request.data["unit_amount"],
                currency=request.data["currency"],
            )
            return Response(price, status=status.HTTP_201_CREATED)
        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CreateCheckoutSessionView(APIView):
    def post(self, request):
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price": request.data["price_id"],
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=request.data["success_url"],
                cancel_url=request.data["cancel_url"],
            )
            return Response(session, status=status.HTTP_201_CREATED)
        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
