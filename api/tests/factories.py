import factory

from api import constants
from api.models import (
    Question,
    # QuestionAnswerEvent,
)


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    type = constants.QUESTION_TYPE_QCM
    difficulty = constants.QUESTION_DIFFICULTY_EASY
    answer_correct = "a"  # constants.QUESTION_ANSWER_CHOICE_LIST[0]
    validation_status = constants.QUESTION_VALIDATION_STATUS_OK
