import random

from django.db.models import Count, F
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api import constants, utilities_notion
from api.models import (
    Question,
    Category,
    Tag,
    Quiz,
    QuestionFeedback,
    QuestionStat,
    QuizStat,
    Contribution,
    DailyStat,
)
from api.serializers import (
    QuestionSerializer,
    CategorySerializer,
    TagSerializer,
    QuizSerializer,
    QuizFullSerializer,
    QuestionFeedbackSerializer,
    QuestionStatSerializer,
    QuizStatSerializer,
    ContributionSerializer,
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
        </ul>
    """
    )


@api_view(["GET"])
def question_list(request):
    """
    List all published questions (return them in a random order)
    Optional query parameters:
    - 'category' (string)
    - 'tag' (string)
    - 'author' (string)
    """
    questions = Question.objects.published().order_by("?")
    if request.GET.get("category"):
        questions = questions.for_category(request.GET.get("category"))
    if request.GET.get("tag"):
        questions = questions.for_tag(request.GET.get("tag"))
    if request.GET.get("author"):
        questions = questions.for_author(request.GET.get("author"))

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

    serializer = QuestionSerializer(question)
    return Response(serializer.data)


@api_view(["POST"])
def question_detail_feedbacks(request, pk):
    """
    Update the question feedbacks
    """
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "POST":
        question_feedback = QuestionFeedback.objects.create(
            question=question,
            choice=request.data["choice"],
            source=request.data["source"],
        )

        serializer = QuestionFeedbackSerializer(question_feedback)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def question_detail_stats(request, pk):
    """
    Update the question stats
    """
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "POST":
        question_stat = QuestionStat.objects.create(
            question=question,
            choice=request.data["choice"],
            source=request.data["source"],
        )

        serializer = QuestionStatSerializer(question_stat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
    questions = Question.objects.published()
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

    serializer = QuestionSerializer(question_random)
    return Response(serializer.data)


@api_view(["GET"])
def question_count(request):
    """
    Retrieve stats on all the data
    """
    # question_publish_stats = (
    #     Question.objects.values("publish")
    #     .annotate(count=Count("publish"))
    #     .order_by("-count")
    # )
    question_publish_count = Question.objects.published().count()

    return Response(question_publish_count)


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
    authors = (
        Question.objects.published()
        .values(name=F("author"))
        .annotate(question_count=Count("author"))
        .order_by("-question_count")
    )

    return Response(list(authors))


@api_view(["GET"])
def difficulty_list(request):
    """
    List all difficulty levels (with the number of questions per difficulty)
    """
    difficulty_levels_query = (
        Question.objects.published()
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
                ),  # noqa
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
    else:
        serializer = QuizSerializer(quizzes, many=True)

    return Response(serializer.data)


@api_view(["POST"])
def quiz_detail_stats(request, pk):
    """
    Update the quiz stats
    """
    try:
        quiz = Quiz.objects.get(pk=pk)
    except Quiz.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "POST":
        quiz_stat = QuizStat.objects.create(
            quiz=quiz, answer_success_count=request.data["answer_success_count"]
        )

        serializer = QuizStatSerializer(quiz_stat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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

        try:
            utilities_notion.add_contribution_row(
                contribution_text=contribution.text,
                contribution_description=contribution.description,
                contribution_type=contribution.type,
            )
        except Exception as e:
            Contribution.objects.create(text=e)

        serializer = ContributionSerializer(contribution)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def stats(request):
    """
    Retrieve stats on all the data
    """
    # question_publish_stats = (
    #     Question.objects.values("publish")
    #     .annotate(count=Count("publish"))
    #     .order_by("-count")
    # )
    question_publish_count = Question.objects.published().count()
    question_validation_status_in_progress_count = Question.objects.for_validation_status(
        constants.QUESTION_VALIDATION_STATUS_IN_PROGRESS
    ).count()
    quiz_publish_stats = (
        Quiz.objects.values("publish")
        .annotate(count=Count("publish"))
        .order_by("-count")
    )
    question_answer_count = (
        QuestionStat.objects.count() + DailyStat.objects.overall_question_answer_count()
    )
    question_category_stats = (
        Category.objects.values("name")
        .annotate(count=Count("questions"))
        .order_by("-count")
    )
    question_tag_stats = (
        Tag.objects.values("name").annotate(count=Count("questions")).order_by("-count")
    )
    question_author_stats = (
        Question.objects.values(name=F("author"))
        .annotate(count=Count("author"))
        .order_by("-count")
    )

    return Response(
        {
            "question_publish_count": question_publish_count,
            "question_validation_status_in_progress_count": question_validation_status_in_progress_count,  # noqa
            "quiz_publish": quiz_publish_stats,
            "answer_count": question_answer_count,
            "category": question_category_stats,
            "tag": question_tag_stats,
            "author": question_author_stats,
            # "answer": question_answer_stats
        }
    )
