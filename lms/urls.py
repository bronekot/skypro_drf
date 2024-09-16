from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, LessonViewSet, SubscriptionView

app_name = "lms"

router = DefaultRouter()
router.register(r"courses", CourseViewSet)
router.register(r"lessons", LessonViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("subscribe/", SubscriptionView.as_view(), name="subscribe"),
]
