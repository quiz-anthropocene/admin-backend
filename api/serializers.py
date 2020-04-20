from rest_framework import serializers

from api.models import (
    Question,
    QuestionCategory,
    QuestionTag,
    Quiz,
    QuestionStat,
    QuizStat,
    Contribution,
)


"""
QUESTION CATEGORY
"""


class QuestionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionCategory
        fields = ["id", "name", "description", "question_count"]


class QuestionCategoryStringSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        return value.name

    class Meta:
        model = QuestionCategory
        fields = ["name"]


"""
QUESTION TAG
"""


class QuestionTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionTag
        fields = ["id", "name", "description", "question_count"]


class QuestionTagStringSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        return value.name

    class Meta:
        model = QuestionTag
        fields = ["name"]


"""
QUESTION
"""


class QuestionSerializer(serializers.ModelSerializer):
    category = QuestionCategoryStringSerializer()
    tags = QuestionTagStringSerializer(many=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "text",
            "type",
            "difficulty",
            "author",
            "category",
            "tags",
            "answer_option_a",
            "answer_option_b",
            "answer_option_c",
            "answer_option_d",
            "has_ordered_answers",
            "answer_correct",
            "answer_explanation",
            "answer_additional_link",
            "answer_image_link",
            "answer_count",
            "answer_success_count",
            "created",
            "updated",
        ]


"""
QUIZ
"""


class QuizSerializer(serializers.ModelSerializer):
    # questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = [
            "id",
            "name",
            "description",
            "author",
            "question_count",
            "categories",
            "tags",
            "created",
        ]


class QuizFullSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = [
            "id",
            "name",
            "description",
            "author",
            "questions",
            "question_count",
            "categories",
            "tags",
            "created",
        ]


"""
QUESTION STATS
"""


class QuestionStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionStat
        fields = ["question_id", "answer_choice", "source", "created"]


"""
QUIZ STATS
"""


class QuizStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizStat
        fields = ["quiz_id", "answer_success_count", "created"]


"""
CONTRIBUTION
"""


class ContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribution
        fields = ["text", "description", "created"]
