import random

from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from api.contributions.serializers import CommentReadSerializer
from api.questions.filters import QuestionFilter
from api.questions.serializers import (
    QuestionDifficultyChoiceSerializer,
    QuestionFullStringSerializer,
    QuestionSerializer,
)
from api.serializers import SimpleChoiceSerializer
from contributions.models import Comment
from core import constants
from questions.models import Question


class QuestionViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Question.objects.public().validated()
    serializer_class = QuestionSerializer
    filterset_class = QuestionFilter

    @extend_schema(summary="Lister toutes les questions *validées*", tags=[Question._meta.verbose_name_plural])
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)

    @extend_schema(summary="Détail d'une question *validée*", tags=[Question._meta.verbose_name_plural])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, args, kwargs)

    @extend_schema(
        summary="Lister tous les commentaires *publiés* d'une question *validée*",
        tags=[Comment._meta.verbose_name_plural],
    )
    @action(detail=True, methods=["get"])
    def contributions(self, request, pk=None):
        question = self.get_object()
        queryset = question.comments_published

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CommentReadSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CommentReadSerializer(queryset, many=True)
        return Response(serializer.data)


class QuestionTypeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = SimpleChoiceSerializer
    queryset = Question.objects.none()

    def get_queryset(self):
        question_types = [{"id": id, "name": name} for (id, name) in constants.QUESTION_TYPE_CHOICES]
        return question_types

    @extend_schema(summary="Lister tous les types de question", tags=[Question._meta.verbose_name_plural])
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)


class QuestionDifficultyViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = QuestionDifficultyChoiceSerializer
    queryset = Question.objects.none()

    def get_queryset(self):
        question_difficulties = [{"id": id, "name": name} for (id, name) in constants.QUESTION_DIFFICULTY_CHOICES]
        return question_difficulties

    @extend_schema(summary="Lister tous les niveaux de difficulté", tags=[Question._meta.verbose_name_plural])
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)


class QuestionLanguageViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = SimpleChoiceSerializer
    queryset = Question.objects.none()

    def get_queryset(self):
        question_languages = [{"id": id, "name": name} for (id, name) in constants.LANGUAGE_CHOICES]
        return question_languages

    @extend_schema(summary="Lister toutes les langues", tags=[Question._meta.verbose_name_plural])
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)


class QuestionValidationStatusViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = SimpleChoiceSerializer
    queryset = Question.objects.none()

    def get_queryset(self):
        question_validation_status = [{"id": id, "name": name} for (id, name) in constants.VALIDATION_STATUS_CHOICES]
        return question_validation_status

    @extend_schema(summary="Lister tous les statuts de validation", tags=[Question._meta.verbose_name_plural])
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)


@api_view(["GET"])
def question_random(request):
    """
    Retrieve a random question
    Optional query parameters:
    - 'current' (question id)
    - 'category' (string)
    - 'tag' (string)
    - // 'author' (string)
    """
    questions = Question.objects.public().validated()
    if request.GET.get("current"):
        questions = questions.exclude(pk=request.GET.get("current"))
    if request.GET.get("category"):
        questions = questions.for_category(request.GET.get("category"))
    if request.GET.get("tag"):
        questions = questions.for_tag(request.GET.get("tag"))
    # if request.GET.get("author"):
    #     questions = questions.for_author(request.GET.get("author"))

    questions_ids = questions.values_list("id", flat=True)
    questions_random_id = random.sample(list(questions_ids), 1)

    question_random = Question.objects.get(pk=questions_random_id[0])

    if request.GET.get("full"):
        serializer = QuestionFullStringSerializer(question_random)
    else:
        serializer = QuestionSerializer(question_random)

    return Response(serializer.data)
