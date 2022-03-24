import factory
from django.utils.text import slugify

from api import constants
from api.models import Question, Quiz, Tag  # QuestionAnswerEvent,
from categories.factories import CategoryFactory


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = "France"


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    text = "La question"
    type = constants.QUESTION_TYPE_QCM
    difficulty = constants.QUESTION_DIFFICULTY_EASY
    language = constants.LANGUAGE_FRENCH
    category = factory.SubFactory(CategoryFactory, name="Energie")
    answer_option_a = "La réponse A"
    answer_option_b = "La réponse B"
    answer_correct = "a"  # constants.QUESTION_ANSWER_CHOICE_LIST[0]
    validation_status = constants.QUESTION_VALIDATION_STATUS_OK


class QuizFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Quiz

    name = "le quiz"
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    publish = False
