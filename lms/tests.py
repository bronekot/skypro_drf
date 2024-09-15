# lms/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from .models import Course, Lesson, Subscription

User = get_user_model()


class LessonTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.course = Course.objects.create(
            title="Test Course", description="Test Description", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            description="Test Description",
            video_link="https://www.youtube.com/watch?v=test",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        url = reverse("lms:lesson-list-create")
        data = {
            "title": "New Lesson",
            "description": "New Description",
            "video_link": "https://www.youtube.com/watch?v=new",
            "course": self.course.id,
            "owner": self.user.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)
        self.assertEqual(Lesson.objects.get(id=response.data["id"]).title, "New Lesson")

    def test_get_lesson(self):
        url = reverse("lms:lesson-detail", kwargs={"pk": self.lesson.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.lesson.title)

    def test_update_lesson(self):
        url = reverse("lms:lesson-detail", kwargs={"pk": self.lesson.id})
        data = {
            "title": "Updated Lesson",
            "description": self.lesson.description,
            "video_link": self.lesson.video_link,
            "course": self.course.id,
            "owner": self.user.id,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Lesson")

    def test_delete_lesson(self):
        url = reverse("lms:lesson-detail", kwargs={"pk": self.lesson.id})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)
