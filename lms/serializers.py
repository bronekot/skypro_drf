from rest_framework import serializers
from .models import Course, Lesson
from .validators import YouTubeURLValidator


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "title", "preview", "description", "lesson_count"]

    def get_lesson_count(self, obj):
        return obj.lessons.count()


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[YouTubeURLValidator()])

    class Meta:
        model = Lesson
        fields = "__all__"
