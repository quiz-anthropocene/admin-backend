import json

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets
from rest_framework.decorators import api_view

from stats.models import (
    DailyStat,
    LinkClickEvent,
    QuestionAnswerEvent,
    QuestionFeedbackEvent,
    QuizAnswerEvent,
    QuizFeedbackEvent,
)
from stats.serializers import (
    LinkClickEventSerializer,
    QuestionAnswerEventSerializer,
    QuestionFeedbackEventSerializer,
    QuizAnswerEventSerializer,
    QuizFeedbackEventSerializer,
)


class QuestionAnswerEventViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = QuestionAnswerEvent.objects.all()
    serializer_class = QuestionAnswerEventSerializer

    @extend_schema(exclude=True)
    def create(self, request, *args, **kwargs):
        return super().create(request, args, kwargs)


class QuestionFeedbackEventViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = QuestionFeedbackEvent.objects.all()
    serializer_class = QuestionFeedbackEventSerializer

    @extend_schema(exclude=True)
    def create(self, request, *args, **kwargs):
        return super().create(request, args, kwargs)


class QuizAnswerEventViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = QuizAnswerEvent.objects.all()
    serializer_class = QuizAnswerEventSerializer

    @extend_schema(exclude=True)
    def create(self, request, *args, **kwargs):
        return super().create(request, args, kwargs)


class QuizFeedbackEventViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = QuizFeedbackEvent.objects.all()
    serializer_class = QuizFeedbackEventSerializer

    @extend_schema(exclude=True)
    def create(self, request, *args, **kwargs):
        return super().create(request, args, kwargs)


class LinkClickEventViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = LinkClickEvent.objects.all()
    serializer_class = LinkClickEventSerializer

    @extend_schema(exclude=True)
    def create(self, request, *args, **kwargs):
        return super().create(request, args, kwargs)


@api_view(["GET"])
def stats_dashboard(request):
    question_answer_count_query = DailyStat.objects.agg_timeseries("question_answer_count", scale="day")
    question_answer_event_count_query = QuestionAnswerEvent.objects.agg_timeseries()
    question_answer_count_list = list(question_answer_count_query) + list(question_answer_event_count_query)
    question_answer_count_json = json.dumps(question_answer_count_list, cls=DjangoJSONEncoder)

    quiz_answer_count_query = DailyStat.objects.agg_timeseries("quiz_answer_count")
    quiz_answer_event_count_query = QuizAnswerEvent.objects.agg_timeseries()
    quiz_answer_count_list = list(quiz_answer_count_query) + list(quiz_answer_event_count_query)
    quiz_answer_count_json = json.dumps(quiz_answer_count_list, cls=DjangoJSONEncoder)

    return render(
        request,
        "stats_dashboard.html",
        {
            "question_answer_count_json": question_answer_count_json,
            "quiz_answer_count_json": quiz_answer_count_json,
        },
    )
