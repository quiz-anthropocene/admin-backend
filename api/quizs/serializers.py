from rest_framework import serializers

from api.questions.serializers import QuestionSerializer
from api.tags.serializers import TagSerializer, TagStringSerializer
from api.users.serializers import UserStringSerializer  # UserSerializer
from quizs.models import Quiz, QuizAuthors, QuizQuestion, QuizRelationship


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


class QuizAuthorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAuthors
        fields = ["id", "quiz", "author"]


class QuizAuthorsInlineSerializer(serializers.ModelSerializer):
    # override QuizAuthors id with author_id
    id = serializers.ReadOnlyField(source="author.id")

    class Meta:
        model = QuizAuthors
        fields = ["id", "quiz", "author"]


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
    "image_background_url",
    "has_audio",
    "author",
    "authors",
    "visibility",
    "validation_status",
    "validator",
    "validation_date",
    "publish",
    "publish_date",
    "spotlight",
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
    class Meta:
        model = Quiz
        fields = QUIZ_FIELDS_WITH_QUESTIONS


class QuizWithQuestionFullStringSerializer(serializers.ModelSerializer):
    tags = TagStringSerializer(many=True)
    author = UserStringSerializer()
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
    author = UserStringSerializer()
    authors = UserStringSerializer(many=True)

    class Meta:
        model = Quiz
        fields = QUIZ_FIELDS_WITH_QUESTIONS


class QuizRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizRelationship
        fields = ["id", "from_quiz", "to_quiz", "status", "created"]
