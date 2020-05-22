from rest_framework import serializers

from api.models import (
    Question,
    Category,
    Tag,
    Quiz,
    QuestionFeedback,
    QuestionStat,
    QuizStat,
    Contribution,
)


"""
QUESTION CATEGORY
"""


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "question_count"]


class CategoryStringSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        return value.name

    class Meta:
        model = Category
        fields = ["name"]


"""
QUESTION TAG
"""


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "description", "question_count"]


class TagStringSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        return value.name

    class Meta:
        model = Tag
        fields = ["name"]


"""
QUESTION
"""


class QuestionSerializer(serializers.ModelSerializer):
    category = CategoryStringSerializer()
    tags = TagStringSerializer(many=True)

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
            "answer_accessible_url",
            "answer_scientific_url",
            "answer_image_url",
            "answer_image_explanation",
            "answer_count",
            "answer_success_count",
            "added",
            "created",
            "updated",
        ]


"""
QUESTION FEEDBACKS
"""


class QuestionFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionFeedback
        fields = ["question_id", "choice", "source", "created"]


"""
QUESTION STATS
"""


class QuestionStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionStat
        fields = ["question_id", "choice", "source", "created"]


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
            "image_background_url",
            "question_count",
            "categories_list",
            "tags_list",
            "difficulty_average",
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
            "image_background_url",
            "questions",
            "question_count",
            "categories_list",
            "tags_list",
            "difficulty_average",
            "created",
        ]


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
        fields = ["text", "description", "type", "created"]
