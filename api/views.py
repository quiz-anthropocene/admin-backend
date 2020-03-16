import random
from django.db.models import Count
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Question, QuestionStat
from api.serializers import QuestionSerializer, QuestionStatSerializer


def api_home(request):
    return HttpResponse("""
        <p>Welcome to the 'Know Your Planet' API.</p>
        <p>Available endpoints:</p>
        <ul>
            <li>GET /api/questions</li>
            <li>GET /api/questions/:id</li>
            <li>GET /api/questions/random</li>
        </ul>
    """)


@api_view(['GET'])
def question_list(request):
    """
    List all questions (return them in a random order)
    """
    questions = Question.objects.exclude(publish=False).order_by("?")

    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
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


@api_view(['POST'])
def question_detail_stats(request, pk):
    """
    Update the question stats
    """
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        question_stat = QuestionStat.objects.create(question=question, answer_choice=request.data['answer_choice'])
        serializer = QuestionStatSerializer(question_stat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def question_random(request):
    """
    Retrieve a random question
    Optional query parameters: 'current' (question id), 'category' (string)
    """
    questions = Question.objects.exclude(publish=False)
    if request.GET.get("current"):
        questions = questions.exclude(pk=request.GET.get("current"))
    if request.GET.get("category"):
        questions = questions.filter(category=request.GET.get("category"))

    questions_ids = questions.values_list('id', flat=True)
    questions_random_id = random.sample(list(questions_ids), 1)

    question_random = Question.objects.get(pk=questions_random_id[0])

    serializer = QuestionSerializer(question_random)
    return Response(serializer.data)


@api_view(['GET'])
def question_stats(request):
    """
    Retrieve stats on all the questions
    """
    question_publish_stats = Question.objects.values("publish").annotate(count=Count("publish")).order_by("-count")
    question_category_stats = Question.objects.values("category").annotate(count=Count("category")).order_by("-count")
    # question_answer_stats = QuestionStat.objects.extra(select={'day': "to_char(created, 'YYYY-MM-DD')"}).values("day").annotate(Count("created"))
    # question_answer_stats = QuestionStat.objects.extra(select={'day': "date(created)"}).values("day").annotate(count=Count("created")) #.order_by("day")
    question_answer_count_stats = QuestionStat.objects.count()
    return Response({
        "publish": question_publish_stats,
        "category": question_category_stats,
        # "answer": question_answer_stats
        "answer_count": question_answer_count_stats
    })
