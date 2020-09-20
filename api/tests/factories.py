import factory

from api import constants
from api.models import (
    Category,
    Tag,
    Question,
    Quiz,
    # QuestionAnswerEvent,
)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ["name"]

    name = "Energie"


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = "France"


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    text = "La question"
    type = constants.QUESTION_TYPE_QCM
    category = factory.SubFactory(CategoryFactory, name="Energie")
    difficulty = constants.QUESTION_DIFFICULTY_EASY
    answer_option_a = "La réponse A"
    answer_option_b = "La réponse B"
    answer_correct = "a"  # constants.QUESTION_ANSWER_CHOICE_LIST[0]
    validation_status = constants.QUESTION_VALIDATION_STATUS_OK
    publish = True


class QuizFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Quiz

    name = "le quiz"
    publish = False
