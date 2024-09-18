from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsModerator, IsOwner

from .models import Course, Lesson, Subscription
from .paginators import StandardResultsSetPagination
from .serializers import CourseSerializer, LessonSerializer


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)
        subscription, created = Subscription.objects.get_or_create(user=user, course=course)
        if not created:
            subscription.delete()
            message = "подписка удалена"
        else:
            message = "подписка добавлена"
        return Response({"message": message})


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def get_queryset(self):
        if self.request.user.is_staff or IsModerator().has_permission(self.request, self):
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListCreate(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def get_queryset(self):
        if self.request.user.is_staff or IsModerator().has_permission(self.request, self):
            return Lesson.objects.all()
        return Lesson.objects.filter(course__owner=self.request.user)

    def perform_create(self, serializer):
        course = serializer.validated_data["course"]
        if course.owner != self.request.user and not (
            self.request.user.is_staff or IsModerator().has_permission(self.request, self)
        ):
            raise permissions.PermissionDenied(
                "У вас нет разрешения на создание уроков для этого курса."
            )
        serializer.save()


class LessonRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def get_queryset(self):
        if self.request.user.is_staff or IsModerator().has_permission(self.request, self):
            return Lesson.objects.all()
        return Lesson.objects.filter(course__owner=self.request.user)
