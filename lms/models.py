from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Course(models.Model):
    title = models.CharField(max_length=200)
    preview = models.ImageField(upload_to="course_previews/", blank=True)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")
    last_update = models.DateTimeField(auto_now=True)

    def is_update_allowed(self):
        if not self.last_update:
            return True
        return (timezone.now() - self.last_update).total_seconds() > 4 * 3600


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    preview = models.ImageField(
        upload_to="lesson_previews/", blank=True, null=True, default=None
    )
    video_link = models.URLField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lessons")


class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscriptions"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="subscriptions"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "course")
