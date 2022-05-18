from rest_framework import serializers

from api.questions.serializers import QuestionSerializer
from api.tags.serializers import TagSerializer
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
    "tags",
    "difficulty_average",
    "language",
    "author",
    "image_background_url",
    "has_audio",
    "publish",
    "spotlight",
    "visibility",
    # "relationships",
    # "question_count",
    # "questions_categories_list",
    # "questions_tags_list",
    # "questions_authors_list",
    "created",
    "updated",
]
QUIZ_FIELDS_WITH_QUESTIONS = QUIZ_FIELDS
QUIZ_FIELDS_WITH_QUESTIONS.insert(QUIZ_FIELDS_WITH_QUESTIONS.index("tags"), "questions")


class QuizSerializer(serializers.ModelSerializer):
    # author = UserStringSerializer()

    class Meta:
        model = Quiz
        fields = QUIZ_FIELDS


class QuizWithQuestionSerializer(serializers.ModelSerializer):
    # author = UserStringSerializer()

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
    author = UserStringSerializer()

    class Meta:
        model = Quiz
        fields = QUIZ_FIELDS_WITH_QUESTIONS


class QuizRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizRelationship
        fields = ["id", "from_quiz", "to_quiz", "status", "created"]