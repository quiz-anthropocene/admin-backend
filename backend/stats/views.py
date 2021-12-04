import json

from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from stats.models import (
    DailyStat,
    QuestionAnswerEvent,
    QuestionFeedbackEvent,
    QuizAnswerEvent,
    QuizFeedbackEvent,
)
from stats.serializers import (
    QuestionAggStatSerializer,
    QuestionAnswerEventSerializer,
    QuestionFeedbackEventSerializer,
    QuizAnswerEventSerializer,
    QuizFeedbackEventSerializer,
)
from api.models import Question, Quiz


def api_home(request):
    return HttpResponse(
        """
        <p>Welcome to the 'Know Your Planet' Stats app.</p>
    """
    )


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
            duration_seconds=request.data["duration_seconds"],
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
