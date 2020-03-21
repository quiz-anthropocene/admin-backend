from rest_framework import serializers
from api.models import Question, QuestionStat


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id', 'text', 'type', 'category', 'difficulty', 'author',
            'answer_option_a', 'answer_option_b', 'answer_option_c', 'answer_option_d',
            'answer_correct', 'answer_explanation', 'answer_additional_links', 'answer_image_link',
            'created', 'updated'
        ]


class QuestionStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionStat
        fields = [
            'question_id', 'answer_choice', 'created'
        ]
