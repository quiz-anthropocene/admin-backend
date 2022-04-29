from django.test import TestCase
from django.urls import reverse

from questions.factories import QuestionFactory
from users.factories import DEFAULT_PASSWORD, UserFactory


QUESTION_DETAIL_URLS = [
    "questions:detail_view",
    "questions:detail_edit",
    "questions:detail_quizs",
    "questions:detail_contributions",
    "questions:detail_stats",
]


class QuestionListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.question_1 = QuestionFactory()
        cls.question_2 = QuestionFactory()

    def test_anonymous_user_cannot_access_question_list(self):
        url = reverse("questions:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/questions/")

    def test_user_can_access_question_list(self):
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
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

    def test_user_can_access_question_detail(self):
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        url = reverse("questions:detail_view", args=[self.question_1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["question"].id, self.question_1.id)
