import json
import random
from io import StringIO

from django.core import management
from django.core.serializers.json import DjangoJSONEncoder
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
    QuestionAnswerEvent,
    QuestionFeedbackEvent,
    Quiz,
    QuizAnswerEvent,
    QuizFeedbackEvent,
    Contribution,
    Glossary,
    DailyStat,
)
from api.serializers import (
    QuestionSerializer,
    QuestionFullStringSerializer,
    CategorySerializer,
    TagSerializer,
    QuizSerializer,
    QuizWithQuestionOrderSerializer,
    QuizFullSerializer,
    QuestionAggStatSerializer,
    QuestionAnswerEventSerializer,
    QuestionFeedbackEventSerializer,
    QuizAnswerEventSerializer,
    QuizFeedbackEventSerializer,
    ContributionSerializer,
    GlossarySerializer,
)


def api_home(request):
    return HttpResponse(
        """
        <p>Welcome to the 'Know Your Planet' API.</p>
        <p>Available endpoints:</p>
        <ul>
            <li>GET /api/questions</li>
            <li>GET /api/questions/:id</li>
            <li>POST /api/questions/:id/stats</li>
            <li>GET /api/questions/random</li>
            <li>GET /api/questions/stats</li>
            <li>GET /api/categories</li>
            <li>GET /api/tags</li>
            <li>GET /api/authors</li>
            <li>GET /api/quizzes</li>
            <li>GET /api/glossary</li>
        </ul>
    """
    )


@api_view(["GET"])
def question_list(request):
    """
    List all validated questions (return them in a semi-random order)
    Optional query parameters:
    - 'category' (string)
    - 'tag' (string)
    - 'author' (string)
    """
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

    return Response(serializer.data)


@api_view(["GET"])
def question_detail(request, pk):
    """
    Retrieve a question
    """
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.GET.get("full"):
        serializer = QuestionFullStringSerializer(question)
    else:
        serializer = QuestionSerializer(question)

    return Response(serializer.data)


@api_view(["GET"])
def question_stats(request, pk):
    """
    Retrieve a question's stats
    """
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = QuestionAggStatSerializer(question.agg_stats)

    return Response(serializer.data)


@api_view(["POST"])
def question_detail_answer_event(request, pk):
    """
    Create a question answer event
    """
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "POST":
        question_answer_event = QuestionAnswerEvent.objects.create(
            question=question,
            choice=request.data["choice"],
            source=request.data["source"],
        )

        serializer = QuestionAnswerEventSerializer(question_answer_event)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def question_detail_feedback_event(request, pk):
    """
    Create a question feedback event
    """
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "POST":
        question_feedback_event = QuestionFeedbackEvent.objects.create(
            question=question,
            choice=request.data["choice"],
            source=request.data["source"],
        )

        serializer = QuestionFeedbackEventSerializer(question_feedback_event)

        # enrich with the agg stats
        question_feedback_count = {
            "like_count_agg": question.like_count_agg,
            "dislike_count_agg": question.dislike_count_agg,
        }
        return Response(
            {**serializer.data, **question_feedback_count},
            status=status.HTTP_201_CREATED,
        )


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


@api_view(["GET"])
def category_list(request):
    """
    List all categories (with the number of questions per category)
    """
    categories = Category.objects.all()

    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def tag_list(request):
    """
    List all tags (with the number of questions per tag)
    """
    tags = Tag.objects.all().order_by("name")

    serializer = TagSerializer(tags, many=True)
    return Response(serializer.data)


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


@api_view(["GET"])
def quiz_list(request):
    """
    List all quizzes (with the number of questions per quiz)
    Optional query parameters:
    - 'author' (string)
    - 'full' (string)
    """
    quizzes = Quiz.objects.published()
    if request.GET.get("author"):
        quizzes = quizzes.for_author(request.GET.get("author"))

    if request.GET.get("full"):
        serializer = QuizFullSerializer(quizzes, many=True)
    elif request.GET.get("question_order"):
        serializer = QuizWithQuestionOrderSerializer(quizzes, many=True)
    else:
        serializer = QuizSerializer(quizzes, many=True)

    return Response(serializer.data)


@api_view(["POST"])
def quiz_detail_answer_event(request, pk):
    """
    Update the quiz answer event
    """
    try:
        quiz = Quiz.objects.get(pk=pk)
    except Quiz.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "POST":
        quiz_answer_event = QuizAnswerEvent.objects.create(
            quiz=quiz,
            question_count=quiz.question_count,
            answer_success_count=request.data["answer_success_count"],
        )

        serializer = QuizAnswerEventSerializer(quiz_answer_event)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def quiz_detail_feedback_event(request, pk):
    """
    Create a quiz feedback event
    """
    try:
        quiz = Quiz.objects.get(pk=pk)
    except Quiz.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "POST":
        quiz_feedback_event = QuizFeedbackEvent.objects.create(
            quiz=quiz, choice=request.data["choice"]
        )

        serializer = QuizFeedbackEventSerializer(quiz_feedback_event)

        # enrich with the agg stats
        quiz_feedback_count = {
            "like_count_agg": quiz.like_count_agg,
            "dislike_count_agg": quiz.dislike_count_agg,
        }
        return Response(
            {**serializer.data, **quiz_feedback_count}, status=status.HTTP_201_CREATED
        )


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


@api_view(["GET"])
def stats_dashboard(request):
    question_answer_count_query = DailyStat.objects.agg_timeseries(
        "question_answer_count", scale="day"
    )
    question_answer_event_count_query = QuestionAnswerEvent.objects.agg_timeseries()
    question_answer_count_list = list(question_answer_count_query) + list(
        question_answer_event_count_query
    )
    question_answer_count_json = json.dumps(
        question_answer_count_list, cls=DjangoJSONEncoder
    )

    quiz_answer_count_query = DailyStat.objects.agg_timeseries("quiz_answer_count")
    quiz_answer_event_count_query = QuizAnswerEvent.objects.agg_timeseries()
    quiz_answer_count_list = list(quiz_answer_count_query) + list(
        quiz_answer_event_count_query
    )
    quiz_answer_count_json = json.dumps(quiz_answer_count_list, cls=DjangoJSONEncoder)

    return render(
        request,
        "stats_dashboard.html",
        {
            "question_answer_count_json": question_answer_count_json,
            "quiz_answer_count_json": quiz_answer_count_json,
        },
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
