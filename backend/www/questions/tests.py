from django.test import TestCase
from django.urls import reverse

from core import constants
from questions.factories import QuestionFactory
from questions.models import Question
from users.factories import DEFAULT_PASSWORD, UserFactory


QUESTION_DETAIL_URLS = [
    "questions:detail_view",
    "questions:detail_edit",
    "questions:detail_quizs",
    "questions:detail_contributions",
    "questions:detail_stats",
    "questions:detail_history",
]


class QuestionListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()
        cls.question_1 = QuestionFactory()
        cls.question_2 = QuestionFactory()

    def test_anonymous_user_cannot_access_question_list(self):
        url = reverse("questions:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/questions/")

    def test_only_contributor_can_access_question_list(self):
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        url = reverse("questions:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        url = reverse("questions:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["questions"]), 2)


class QuestionDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.question_1 = QuestionFactory()
        cls.question_2 = QuestionFactory()

    def test_anonymous_user_cannot_access_question_detail(self):
        for edit_url in QUESTION_DETAIL_URLS:
            url = reverse(edit_url, args=[self.question_1.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_contributor_can_access_question_detail(self):
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        url = reverse("questions:detail_view", args=[self.question_1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["question"].id, self.question_1.id)


class QuestionCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()

    def test_anonymous_user_cannot_access_question_create(self):
        url = reverse("questions:create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_only_contributor_can_access_question_list(self):
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        url = reverse("questions:create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        url = reverse("questions:create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_contributor_can_create_question(self):
        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        url = reverse("questions:create")
        data = {
            "text": "Question 1",
            "type": constants.QUESTION_TYPE_QCM,
            "difficulty": constants.QUESTION_DIFFICULTY_EASY,
            "language": constants.LANGUAGE_FRENCH,
            "answer_option_a": "Réponse A",
            "answer_option_b": "Réponse B",
            "answer_correct": "a",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)  # 201
        self.assertEqual(Question.objects.count(), 1)
