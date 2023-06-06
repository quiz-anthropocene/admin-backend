from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from activity.models import Event
from activity.utilities import create_event
from questions.factories import QuestionFactory
from quizs.factories import QuizFactory
from users import constants as user_constants
from users.factories import UserFactory


class EventUtilitiesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_contributor = UserFactory()
        cls.user_admin = UserFactory(roles=[user_constants.USER_ROLE_ADMINISTRATOR])
        cls.question = QuestionFactory()
        cls.quiz = QuizFactory()

    def test_create_event(self):
        create_event(user=self.user_contributor, event_verb="CREATED", event_object=self.question)
        create_event(user=self.user_contributor, event_verb="CREATED", event_object=self.quiz)
        create_event(
            user=self.user_admin,
            event_verb="VALIDATED",
            event_object=self.question,
            created=timezone.now() + timedelta(days=1),
        )
        create_event(
            user=self.user_admin,
            event_verb="PUBLISHED",
            event_object=self.quiz,
            created=timezone.now() + timedelta(days=2),
        )
        self.assertEqual(Event.objects.count(), 4)
        self.assertEqual(Event.objects.filter(created__lte=timezone.now()).count(), 2)

    def test_create_event_weekly_agg_stat(self):
        extra_data = {
            "event_object_type": "WEEKLY_AGG_STAT",
            "question_answer_count": 2,
            "quiz_answer_count": 1,
            "question_feedback_count": 0,
            "quiz_feedback_count": 0,
        }
        create_event(user=None, event_verb="COMPUTED", extra_data=extra_data)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Event.objects.first().event_object_type, "WEEKLY_AGG_STAT")
        self.assertTrue("event_object_type" not in Event.objects.first().extra_data.keys())
        self.assertTrue("question_answer_count" in Event.objects.first().extra_data.keys())
