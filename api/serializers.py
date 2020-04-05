from rest_framework import serializers

from api.models import Question, QuestionCategory, QuestionTag, QuestionStat, Contribution


class QuestionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionCategory
        fields = [
            'id', 'name', 'description',
            'question_count'
        ]

class QuestionCategoryStringSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        return value.name

    class Meta:
        model = QuestionCategory
        fields = [
            'name'
        ]


class QuestionTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionTag
        fields = [
            'id', 'name', 'description',
            'question_count'
        ]

class QuestionTagStringSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        return value.name

    class Meta:
        model = QuestionTag
        fields = [
            'name'
        ]


class QuestionSerializer(serializers.ModelSerializer):
    category = QuestionCategoryStringSerializer()
    tags = QuestionTagStringSerializer(many=True)

    class Meta:
        model = Question
        fields = [
            'id', 'text', 'type', 'difficulty', 'author',
            'category', 'tags',
            'answer_option_a', 'answer_option_b', 'answer_option_c', 'answer_option_d',
            'answer_correct', 'answer_explanation', 'answer_additional_link', 'answer_image_link',
            'answer_count', 'answer_success_count',
            'created', 'updated'
        ]


class QuestionStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionStat
        fields = [
            'question_id', 'answer_choice', 'created'
        ]

class ContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribution
        fields = [
            'text', 'description', 'created'
        ]