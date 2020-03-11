import random
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Question
from api.serializers import QuestionSerializer


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


@api_view(['GET'])
def question_random(request):
    """
    Retrieve a random question
    Optional query parameters: 'current'
    """
    questions = Question.objects.exclude(publish=False)
    if request.GET.get("current"):
        questions = questions.exclude(pk=request.GET.get("current"))

    questions_ids = questions.values_list('id', flat=True)
    questions_random_id = random.sample(list(questions_ids), 1)

    question_random = Question.objects.get(pk=questions_random_id[0])

    serializer = QuestionSerializer(question_random)
    return Response(serializer.data)
