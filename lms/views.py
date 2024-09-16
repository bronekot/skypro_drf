import uuid

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from rest_framework import generics, permissions, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsModerator, IsOwner

from .models import Course, Lesson, Subscription
from .paginators import StandardResultsSetPagination
from .serializers import CourseSerializer, LessonSerializer
from .tasks import send_course_update_email  # Им


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
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        course = self.get_object()
        subscriptions = Subscription.objects.filter(course=course)
        for subscription in subscriptions:
            send_course_update_email.delay(subscription.user.email, course.name)
        return response


class LessonListCreate(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]


class LessonRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]


def send_test_email(request):
    subject = "Тестовое письмо"
    message = "Это тестовое письмо для проверки настройки отправки email."
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = ["demondzr@yandex.ru"]
    email = EmailMessage(subject, message, email_from, recipient_list)
    email.extra_headers = {"Message-ID": "<{}@example.com>".format(uuid.uuid4())}
    email.send()
    return HttpResponse("Тестовое письмо отправлено.")
