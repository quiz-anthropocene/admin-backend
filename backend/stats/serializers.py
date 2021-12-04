from rest_framework import serializers

from stats.models import (
    QuestionAggStat,
    QuestionAnswerEvent,
    QuestionFeedbackEvent,
    QuizAnswerEvent,
    QuizFeedbackEvent,
)


"""
QUESTION AGG STATS
"""


class QuestionAggStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAggStat
        fields = [
            "question_id",
            "answer_count",
            "answer_success_count",
            "like_count",
            "dislike_count",
        ]


"""
QUESTION ANSWER EVENT
"""


class QuestionAnswerEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswerEvent
        fields = ["question_id", "choice", "source", "created"]


"""
QUESTION FEEDBACK EVENT
"""


class QuestionFeedbackEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionFeedbackEvent
        fields = ["question_id", "choice", "source", "created"]


"""
QUIZ ANSWER EVENT
"""


class QuizAnswerEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAnswerEvent
        fields = ["quiz_id", "question_count", "answer_success_count", "duration_seconds", "created"]


"""
QUIZ FEEDBACK EVENT
"""


class QuizFeedbackEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizFeedbackEvent
        fields = ["quiz_id", "choice", "created"]
