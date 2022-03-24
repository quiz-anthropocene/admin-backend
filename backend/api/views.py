import json
import random
from io import StringIO

from django.core import management
from django.db.models import Count, F
from django.http import HttpResponse
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api import constants, utilities_sendinblue
from api.filters import QuestionFilter, QuizFilter
from api.models import Question, Quiz, Tag
from api.serializers import (
    QuestionDifficultyChoiceSerializer,
    QuestionFullStringSerializer,
    QuestionSerializer,
    QuizSerializer,
    SimpleChoiceSerializer,
    TagSerializer,
)


def api_home(request):
    return HttpResponse(
        """
        <p>API du Quiz de l'Anthropocène.</p>
        <p>La documentation se trouve à l'adresse <a href="/api/docs/">/api/docs/</a></p>
        """
    )


class QuestionViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Question.objects.validated()
    serializer_class = QuestionSerializer
    filter_class = QuestionFilter

    @extend_schema(summary="Lister toutes les questions *validées*", tags=[Question._meta.verbose_name_plural])
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)

    @extend_schema(summary="Détail d'une question *validée*", tags=[Question._meta.verbose_name_plural])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, args, kwargs)


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
        question_validation_status = [
            {"id": id, "name": name} for (id, name) in constants.QUESTION_VALIDATION_STATUS_CHOICES
        ]
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
    - 'author' (string)
    """
    questions = Question.objects.validated()
    if request.GET.get("current"):
        questions = questions.exclude(pk=request.GET.get("current"))
    if request.GET.get("category"):
        questions = questions.for_category(request.GET.get("category"))
    if request.GET.get("tag"):
        questions = questions.for_tag(request.GET.get("tag"))
    if request.GET.get("author"):
        questions = questions.for_author(request.GET.get("author"))

    questions_ids = questions.values_list("id", flat=True)
    questions_random_id = random.sample(list(questions_ids), 1)

    question_random = Question.objects.get(pk=questions_random_id[0])

    if request.GET.get("full"):
        serializer = QuestionFullStringSerializer(question_random)
    else:
        serializer = QuestionSerializer(question_random)

    return Response(serializer.data)


class TagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Tag.objects.all().order_by("name")
    serializer_class = TagSerializer

    @extend_schema(summary="Lister tous les tags", tags=[Tag._meta.verbose_name_plural])
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)


@api_view(["GET"])
def author_list(request):
    """
    List all authors (with the number of questions per author)
    """
    question_authors = (
        Question.objects.validated()
        .values(name=F("author"))
        .annotate(question_count=Count("author"))
        .order_by("-question_count")
    )

    return Response(list(question_authors))


class QuizViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Quiz.objects.published()
    serializer_class = QuizSerializer
    filter_class = QuizFilter

    @extend_schema(summary="Lister tous les quiz *publiés*", tags=[Quiz._meta.verbose_name_plural])
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)

    @extend_schema(summary="Détail d'un quiz *publié*", tags=[Quiz._meta.verbose_name_plural])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, args, kwargs)


@api_view(["GET", "POST"])
def notion_questions(request):
    notion_questions_validation = []

    if request.POST.get("run_validate_questions_in_notion_script", False):
        out = StringIO()
        management.call_command("validate_questions_in_notion", stdout=out)
        notion_questions_validation = out.getvalue()
        notion_questions_validation = notion_questions_validation.split("\n")

    return render(
        request,
        "notion_questions.html",
        {"notion_questions_validation": notion_questions_validation},
    )


@api_view(["POST"])
def newsletter(request):
    if request.method == "POST":
        try:
            response = utilities_sendinblue.newsletter_registration(request.data["email"])
            if response.status_code != 201:
                raise Exception(json.loads(response._content))
            success_message = (
                "Votre inscription a été reçu, merci ! "
                "Vous allez reçevoir un email pour confirmer votre inscription."
            )
            return Response(success_message, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_message = f"Erreur lors de votre inscription à la newsletter. {e}"
            return Response(error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
