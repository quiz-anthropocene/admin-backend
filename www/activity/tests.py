from django.test import TestCase
from django.urls import reverse

from activity.factories import EventFactory
from questions.factories import QuestionFactory
from quizs.factories import QuizFactory
from users import constants as user_constants
from users.factories import DEFAULT_PASSWORD, UserFactory


class EventListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("activity:list")
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()
        cls.user_admin = UserFactory(roles=[user_constants.USER_ROLE_ADMINISTRATOR])
        cls.question = QuestionFactory(author=cls.user_contributor)
        cls.quiz = QuizFactory()  # authors=[cls.user_contributor]
        cls.quiz.authors.set([cls.user_contributor])
        cls.event_item_1 = EventFactory(
            actor_id=cls.user_admin.id,
            event_verb="CREATED",
            event_object_id=cls.user_contributor.id,
            event_object_type="USER",
        )
        cls.event_item_1 = EventFactory(
            actor_id=cls.user_contributor.id,
            event_verb="CREATED",
            event_object_id=cls.question.id,
            event_object_type="QUESTION",
        )
        cls.event_item_2 = EventFactory(
            actor_id=cls.user_contributor.id,
            event_verb="CREATED",
            event_object_id=cls.quiz.id,
            event_object_type="QUIZ",
        )
        cls.event_item_2 = EventFactory(
            actor_id=cls.user_admin.id, event_verb="PUBLISHED", event_object_id=cls.quiz.id, event_object_type="QUIZ"
        )

    def test_only_contributor_can_access_event_list(self):
        # anonymous
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/?next=", response.url)
        # simple user
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        # contributor
        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["events"]), 1 + 1)
