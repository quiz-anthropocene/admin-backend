from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from activity.models import Event
from activity.utilities import create_event
from questions.factories import QuestionFactory
from users import constants as user_constants
from users.factories import UserFactory


class EventUtilitiesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_contributor = UserFactory()
        cls.user_admin = UserFactory(roles=[user_constants.USER_ROLE_ADMINISTRATOR])
        cls.question = QuestionFactory()

    def test_create_event(self):
        create_event(user=self.user_contributor, event_verb="CREATED", event_object=self.question)
        self.assertEqual(Event.objects.count(), 1)
        create_event(
            user=self.user_admin,
            event_verb="VALIDATED",
            event_object=self.question,
            created=timezone.now() + timedelta(days=1),
        )
        self.assertEqual(Event.objects.count(), 2)
        self.assertEqual(Event.objects.filter(created__lte=timezone.now()).count(), 1)
