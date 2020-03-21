import random
import requests
import json

from django.conf import settings
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
    body parameters:
    - 'answer_choice' (string)
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
    query parameters:
    - 'current' (question id) [optional]
    - 'category' (string) [optional]
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


@api_view(['POST'])
def question_contribute(request):
    """
    Contribute a new question
    body params:
    - 'question_text' (string) (string)
    - 'additional_info' (string) [optional]
    """
    GITHUB_API_URL = "https://api.github.com/repos/raphodn/know-your-planet/issues"

    # process data
    contribution_issue_title = request.data['question_text'] if (len(request.data['question_text']) < 50) else (request.data['question_text'][0:47] + "...")
    payload = {
        "title": contribution_issue_title,
        "body": f"<h2>La question</h2><p>{request.data['question_text']}</p><h2>Explications</h2><p>{request.data['additional_info']}</p>",
        "labels": ["Contribution"]
    }

    # query github api
    headers = {
        "Authorization": f"token {settings.GITHUB_API_TOKEN}",
        "Accept": "application/vnd.github.machine-man-preview"
    }
    response = requests.request("POST", GITHUB_API_URL, data=json.dumps(payload), headers=headers)
    
    # process response
    response_data = response.json()
    if response.status_code == 201:
        return Response({
            "status": status.HTTP_201_CREATED,
            "github_issue_url": response_data["html_url"]
        })
    else:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": response_data["message"]
        })
