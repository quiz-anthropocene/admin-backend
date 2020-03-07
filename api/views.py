from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Question
from api.serializers import QuestionSerializer


@api_view(['GET'])
def question_list(request):
    """
    List all questions
    """
    questions = Question.objects.all()
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
