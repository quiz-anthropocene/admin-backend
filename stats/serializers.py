from rest_framework import serializers

from questions.models import Question
from quizs.models import Quiz
from stats.models import LinkClickEvent, QuestionAnswerEvent, QuestionFeedbackEvent, QuizAnswerEvent, QuizFeedbackEvent


# class QuestionAggStatSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = QuestionAggStat
#         fields = [
#             "question_id",
#             "answer_count",
#             "answer_success_count",
#             "like_count",
#             "dislike_count",
#         ]


class QuestionAnswerEventSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), required=True)

    class Meta:
        model = QuestionAnswerEvent
        fields = ["question", "choice", "source", "quiz", "created"]


class QuestionFeedbackEventSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), required=True)

    class Meta:
        model = QuestionFeedbackEvent
        fields = ["question", "choice", "source", "quiz", "created"]


class QuizAnswerEventSerializer(serializers.ModelSerializer):
    quiz = serializers.PrimaryKeyRelatedField(queryset=Quiz.objects.all(), required=True)

    class Meta:
        model = QuizAnswerEvent
        fields = [
            "quiz",
            "question_count",
            "answer_success_count",
            "duration_seconds",
            "question_answer_split",
            "created",
        ]


class QuizFeedbackEventSerializer(serializers.ModelSerializer):
    quiz = serializers.PrimaryKeyRelatedField(queryset=Quiz.objects.all(), required=True)

    class Meta:
        model = QuizFeedbackEvent
        fields = ["quiz", "choice", "created"]


class LinkClickEventSerializer(serializers.ModelSerializer):
    quiz = serializers.PrimaryKeyRelatedField(queryset=Quiz.objects.all(), required=False)
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), required=False)

    class Meta:
        model = LinkClickEvent
        fields = ["quiz", "question", "link_url", "created"]
