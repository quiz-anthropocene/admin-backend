from rest_framework import serializers

from api.models import (
    Category,
    Tag,
    Question,
    QuestionAggStat,
    QuestionAnswerEvent,
    QuestionFeedbackEvent,
    Quiz,
    QuizAnswerEvent,
    QuizFeedbackEvent,
    Contribution,
    Glossary,
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

QUESTION_FIELDS = [
    "id",
    "text",
    "hint",
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
    "answer_count_agg",
    "answer_success_count_agg",
    "added",
    "created",
    "updated",
]


class QuestionSerializer(serializers.ModelSerializer):
    # category = CategoryStringSerializer()
    # tags = TagStringSerializer(many=True)

    class Meta:
        model = Question
        fields = QUESTION_FIELDS


class QuestionFullStringSerializer(serializers.ModelSerializer):
    category = CategoryStringSerializer()
    tags = TagStringSerializer(many=True)

    class Meta:
        model = Question
        fields = QUESTION_FIELDS


class QuestionFullObjectSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Question
        fields = QUESTION_FIELDS


"""
QUESTION AGG STATS
"""


class QuestionAggStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAggStat
        fields = [
            "question_id",
            "answer_count",
            "answer_success_count",
            "like_count",
            "dislike_count",
        ]


"""
QUESTION ANSWER EVENT
"""


class QuestionAnswerEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswerEvent
        fields = ["question_id", "choice", "source", "created"]


"""
QUESTION FEEDBACK EVENT
"""


class QuestionFeedbackEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionFeedbackEvent
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
            "introduction",
            "conclusion",
            "author",
            "image_background_url",
            "questions",
            "tags",
            "question_count",
            "questions_categories_list",
            "questions_tags_list",
            "questions_authors_list",
            "difficulty_average",
            "created",
        ]


class QuizFullSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Quiz
        fields = [
            "id",
            "name",
            "introduction",
            "conclusion",
            "author",
            "image_background_url",
            "questions",
            "tags",
            "question_count",
            "questions_categories_list",
            "questions_tags_list",
            "questions_authors_list",
            "difficulty_average",
            "created",
        ]


"""
QUIZ ANSWER EVENT
"""


class QuizAnswerEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAnswerEvent
        fields = ["quiz_id", "question_count", "answer_success_count", "created"]


"""
QUIZ FEEDBACK EVENT
"""


class QuizFeedbackEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizFeedbackEvent
        fields = ["quiz_id", "choice", "created"]


"""
CONTRIBUTION
"""


class ContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribution
        fields = ["text", "description", "type", "created"]


"""
GLOSSARY
"""


class GlossarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Glossary
        fields = [
            "name",
            "name_alternatives",
            "definition_short",
            "description",
            "description_accessible_url",
            "added",
            "created",
        ]
