from rest_framework import serializers

from api.questions.serializers import QuestionSerializer
from api.tags.serializers import TagSerializer, TagStringSerializer
from api.users.serializers import UserStringSerializer  # UserSerializer
from quizs.models import Quiz, QuizQuestion, QuizRelationship


class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = ["id", "quiz", "question", "order", "created"]


class QuizQuestionInlineSerializer(serializers.ModelSerializer):
    # override QuizQuestion id with question_id
    id = serializers.ReadOnlyField(source="question.id")

    class Meta:
        model = QuizQuestion
        fields = ["id", "order"]


QUIZ_FIELDS = [
    "id",
    "name",
    "slug",
    "introduction",
    "conclusion",
    # "questions",
    # "question_count",
    "tags",
    "difficulty_average",
    "language",
    "image_background_url",
    "has_audio",
    "authors",
    "visibility",
    "validation_status",
    "validator",
    "validation_date",
    "publish",
    "publish_date",
    "spotlight",
    # "relationships",
    # "questions_categories_list",
    # "questions_tags_list",
    # "questions_authors_list",
    "created",
    "updated",
]

QUIZ_FIELDS_WITH_QUESTION_COUNT = QUIZ_FIELDS.copy()
QUIZ_FIELDS_WITH_QUESTION_COUNT.insert(QUIZ_FIELDS_WITH_QUESTION_COUNT.index("tags"), "question_count")

QUIZ_FIELDS_WITH_QUESTIONS = QUIZ_FIELDS.copy()
QUIZ_FIELDS_WITH_QUESTIONS.insert(QUIZ_FIELDS_WITH_QUESTIONS.index("tags"), "questions")

QUIZ_FIELDS_WITH_QUESTION_COUNT_AND_QUESTIONS = QUIZ_FIELDS_WITH_QUESTION_COUNT.copy()
QUIZ_FIELDS_WITH_QUESTION_COUNT_AND_QUESTIONS.insert(
    QUIZ_FIELDS_WITH_QUESTION_COUNT_AND_QUESTIONS.index("question_count"), "questions"
)


class QuizSerializer(serializers.ModelSerializer):
    # author = UserStringSerializer()
    question_count = serializers.IntegerField(source="questions.count", read_only=True)

    class Meta:
        model = Quiz
        fields = QUIZ_FIELDS_WITH_QUESTION_COUNT


class QuizWithQuestionSerializer(serializers.ModelSerializer):
    question_count = serializers.IntegerField(source="questions.count", read_only=True)

    class Meta:
        model = Quiz
        fields = QUIZ_FIELDS_WITH_QUESTION_COUNT_AND_QUESTIONS


class QuizWithQuestionFullStringSerializer(serializers.ModelSerializer):
    tags = TagStringSerializer(many=True)
    authors = UserStringSerializer(many=True)

    class Meta:
        model = Quiz
        fields = QUIZ_FIELDS_WITH_QUESTIONS


class QuizWithQuestionOrderSerializer(serializers.ModelSerializer):
    questions = QuizQuestionInlineSerializer(source="quizquestion_set", many=True)

    class Meta:
        model = Quiz
        fields = QUIZ_FIELDS_WITH_QUESTIONS


class QuizFullSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    tags = TagSerializer(many=True)
    authors = UserStringSerializer(many=True)

    class Meta:
        model = Quiz
        fields = QUIZ_FIELDS_WITH_QUESTIONS


class QuizRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizRelationship
        fields = ["id", "from_quiz", "to_quiz", "status", "created"]
