from rest_framework import serializers
from api.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id', 'text', 'type', 'category', 'difficulty',
            'answer_option_a', 'answer_option_b', 'answer_option_c', 'answer_option_d',
            'answer_correct', 'answer_explanation', 'answer_additional_links',
            'created', 'updated'
        ]
