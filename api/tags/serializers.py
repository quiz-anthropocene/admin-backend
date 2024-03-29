from rest_framework import serializers

from tags.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            "id",
            "name",
            "description",
            "created",
        ]  # "question_count", "question_public_validated_count", "updated"


class TagStringSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        return value.name

    class Meta:
        model = Tag
        fields = ["name"]
