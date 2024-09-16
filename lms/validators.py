import re

from rest_framework import serializers


class YouTubeURLValidator:
    message = "Ссылка должна быть на youtube.com"
    code = "invalid"

    def __call__(self, value):
        youtube_regex = re.compile(
            r"^(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$"
        )
        if not youtube_regex.match(value):
            raise serializers.ValidationError(self.message, code=self.code)
