from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            # "email", "roles"
            "created",
        ]  # "question_count", "quiz_count", "updated"


class UserWithCountSerializer(serializers.ModelSerializer):
    question_count = serializers.IntegerField(source="question_public_validated_count")
    quiz_count = serializers.IntegerField(source="quiz_published_count")

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            # "email", "roles"
            "question_count",
            "quiz_count",
            "created",
        ]  # "updated"


class UserStringSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        return value.full_name

    class Meta:
        model = User
        fields = ["full_name"]
