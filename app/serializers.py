from rest_framework import serializers

from app.models import User, Question, Answer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "bio",
            "student",
        )
        read_only_fields = ("id",)
        write_only_fields = ("password",)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"
        read_only_fields = ("id",)


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"
        read_only_fields = ("id",)
