from django.test import TestCase
from django.urls import reverse

from core import constants
from quizs.factories import QuizFactory
from quizs.models import Quiz
from users.factories import DEFAULT_PASSWORD, UserFactory


QUIZ_DETAIL_URLS = [
    "quizs:detail_view",
    "quizs:detail_edit",
    "quizs:detail_questions",
    "quizs:detail_contributions",
    "quizs:detail_stats",
    "quizs:detail_history",
]


class QuizListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()
        cls.quiz_1 = QuizFactory(name="Quiz 1")
        cls.quiz_2 = QuizFactory(name="Quiz 2")

    def test_anonymous_user_cannot_access_quiz_list(self):
        url = reverse("quizs:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/quizs/")

    def test_only_contributor_can_access_quiz_list(self):
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        url = reverse("quizs:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        url = reverse("quizs:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["quizs"]), 2)


class QuizDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.quiz_1 = QuizFactory(name="Quiz 1")
        cls.quiz_2 = QuizFactory(name="Quiz 2")

    def test_anonymous_user_cannot_access_quiz_detail(self):
        for edit_url in QUIZ_DETAIL_URLS:
            url = reverse(edit_url, args=[self.quiz_1.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_contributor_can_access_quiz_detail(self):
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        url = reverse("quizs:detail_view", args=[self.quiz_1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["quiz"].id, self.quiz_1.id)


class QuizCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()

    def test_anonymous_user_cannot_access_quiz_create(self):
        url = reverse("quizs:create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_only_contributor_can_access_quiz_create(self):
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        url = reverse("quizs:create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        url = reverse("quizs:create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_contributor_can_create_quiz(self):
        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        url = reverse("quizs:create")
        data = {"name": "Quiz 1", "language": constants.LANGUAGE_FRENCH}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)  # 201
        self.assertEqual(Quiz.objects.count(), 1)
