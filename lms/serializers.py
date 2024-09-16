from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import YouTubeURLValidator


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["user", "course", "created_at"]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "preview",
            "description",
            "lesson_count",
            "is_subscribed",
            "lessons",
        ]

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        return Subscription.objects.filter(user=user, course=obj).exists()


class LessonSerializer(serializers.ModelSerializer):
    video_link = serializers.URLField(validators=[YouTubeURLValidator()])

    class Meta:
        model = Lesson
        fields = "__all__"
