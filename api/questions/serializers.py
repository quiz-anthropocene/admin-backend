from rest_framework import serializers

from api.categories.serializers import CategorySerializer, CategoryStringSerializer
from api.tags.serializers import TagSerializer, TagStringSerializer
from api.users.serializers import UserStringSerializer  # UserSerializer
from questions.models import Question


class QuestionDifficultyChoiceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


QUESTION_FIELDS = [
    "id",
    "text",
    "hint",
    "type",
    "category",
    "tags",
    "difficulty",
    "language",
    "answer_choice_a",
    "answer_choice_b",
    "answer_choice_c",
    "answer_choice_d",
    "answer_correct",
    "has_ordered_answers",
    "answer_explanation",
    "answer_audio_url",
    "answer_audio_url_text",
    "answer_video_url",
    "answer_video_url_text",
    "answer_source_accessible_url",
    "answer_source_accessible_url_text",
    "answer_source_scientific_url",
    "answer_source_scientific_url_text",
    "answer_book_recommendation",
    "answer_image_url",
    "answer_image_url_text",
    "answer_extra_info",
    "author",
    "visibility",
    "validation_status",
    "validator",
    "validation_date",
    "created",
    "updated",
    # "answer_count_agg",
    # "answer_success_count_agg",
]


class QuestionSerializer(serializers.ModelSerializer):
    # author = UserStringSerializer()
    # validator = UserStringSerializer()

    class Meta:
        model = Question
        fields = QUESTION_FIELDS


class QuestionFullStringSerializer(serializers.ModelSerializer):
    category = CategoryStringSerializer()
    tags = TagStringSerializer(many=True)
    author = UserStringSerializer()
    validator = UserStringSerializer()

    class Meta:
        model = Question
        fields = QUESTION_FIELDS


class QuestionFullObjectSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Question
        fields = QUESTION_FIELDS
