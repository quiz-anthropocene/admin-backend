import json
import random
from io import StringIO
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets

from django.core import management
from django.db.models import Count, F
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api import constants, utilities_sendinblue
from api.models import (
    Category,
    Tag,
    Question,
    Quiz,
    Contribution,
    Glossary,
)
from api.serializers import (
    QuestionSerializer,
    QuestionFullStringSerializer,
    CategorySerializer,
    TagSerializer,
    QuizSerializer,
    QuizWithQuestionOrderSerializer,
    QuizFullSerializer,
    ContributionSerializer,
    GlossarySerializer,
)


def api_home(request):
    return HttpResponse(
        """
        <p>API du Quiz de l'Anthropocène.</p>
        <p>La documentation se trouve à l'adresse <a href="/api/docs/">/api/docs/</a></p>
        """
    )


class QuestionViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    TODO: implement filters

    # get only the validated questions
    questions = Question.objects.validated()

    # order by difficulty, then random inside
    questions = questions.order_by("difficulty", "?")

    # filters
    if request.GET.get("category"):
        questions = questions.for_category(request.GET.get("category"))
    if request.GET.get("tag"):
        questions = questions.for_tag(request.GET.get("tag"))
    if request.GET.get("author"):
        questions = questions.for_author(request.GET.get("author"))

    if request.GET.get("full"):
        serializer = QuestionFullStringSerializer(questions, many=True)
    else:
        serializer = QuestionSerializer(questions, many=True)
    """
    queryset = Question.objects.validated()
    serializer_class = QuestionSerializer

    @extend_schema(summary="Lister toutes les questions", tags=[Question._meta.verbose_name_plural])
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)

    @extend_schema(summary="Détail d'une question", tags=[Question._meta.verbose_name_plural])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, args, kwargs)


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


@api_view(["GET"])
def question_count(request):
    """
    Retrieve stats on all the data
    """
    question_validated_count = Question.objects.validated().count()

    return Response(question_validated_count)


class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @extend_schema(summary="Lister toutes les catégories", tags=[Category._meta.verbose_name_plural])
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)


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


@api_view(["GET"])
def difficulty_level_list(request):
    """
    List all difficulty levels (with the number of questions per difficulty)
    """
    difficulty_levels_query = (
        Question.objects.validated()
        .values(value=F("difficulty"))
        .annotate(question_count=Count("difficulty"))
    )

    difficulty_levels = []
    for x, y in constants.QUESTION_DIFFICULTY_CHOICES:
        difficulty_levels.append(
            {
                "name": y,
                "value": x,
                "question_count": next(
                    (
                        item["question_count"]
                        for item in difficulty_levels_query
                        if item["value"] == x
                    ),
                    0,
                ),
            }
        )

    return Response(difficulty_levels)


class QuizViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    TODO: implement filters

    quizzes = Quiz.objects.published()
    if request.GET.get("author"):
        quizzes = quizzes.for_author(request.GET.get("author"))

    if request.GET.get("full"):
        serializer = QuizFullSerializer(quizzes, many=True)
    elif request.GET.get("question_order"):
        serializer = QuizWithQuestionOrderSerializer(quizzes, many=True)
    else:
        serializer = QuizSerializer(quizzes, many=True)
    """
    queryset = Quiz.objects.published()
    serializer_class = QuizSerializer

    @extend_schema(summary="Lister tous les quiz", tags=[Quiz._meta.verbose_name_plural])
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)

    @extend_schema(summary="Détail d'un quiz", tags=[Quiz._meta.verbose_name_plural])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, args, kwargs)


@api_view(["POST"])
def contribute(request):
    """
    Add a contribution
    """
    if request.method == "POST":
        contribution = Contribution.objects.create(
            text=request.data["text"],
            description=request.data["description"],
            type=request.data["type"],
        )

        # send to Notion ?
        # done with export_contributions_to_notion + cron_export_contributions_to_notion  # noqa

        serializer = ContributionSerializer(contribution)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def glossary_list(request):
    """
    List all glossary entries
    """
    glossary = Glossary.objects.all().order_by("name")

    serializer = GlossarySerializer(glossary, many=True)
    return Response(serializer.data)


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
            response = utilities_sendinblue.newsletter_registration(
                request.data["email"]
            )
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
