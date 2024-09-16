from django.utils import timezone
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from .permissions import IsOwner, IsModerator
from .tasks import send_course_update_email


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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_update_allowed():
            response = super().update(request, *args, **kwargs)
            if response.status_code == status.HTTP_200_OK:
                subscriptions = Subscription.objects.filter(course=instance)
                for subscription in subscriptions:
                    send_course_update_email.delay(
                        subscription.user.email, instance.title
                    )
            instance.last_update = timezone.now()
            instance.save()
            return response
        else:
            return Response(
                {"detail": "Course was updated less than 4 hours ago."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )


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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        course = instance.course
        if course.is_update_allowed():
            response = super().update(request, *args, **kwargs)
            if response.status_code == status.HTTP_200_OK:
                subscriptions = Subscription.objects.filter(course=course)
                for subscription in subscriptions:
                    send_course_update_email.delay(
                        subscription.user.email,
                        f"Урок '{instance.title}' в курсе '{course.title}' был обновлен.",
                    )
                course.last_update = timezone.now()
                course.save()
            return response
        else:
            return Response(
                {
                    "detail": "Course was updated less than 4 hours ago. Lesson update not allowed."
                },
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )


class SubscriptionView(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response(
                {
                    "detail": "You do not have permission to unsubscribe from this course."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)
