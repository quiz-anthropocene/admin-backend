import factory

from categories.factories import CategoryFactory
from core import constants
from questions.models import Question


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
