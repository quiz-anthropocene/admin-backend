from django.test import TestCase
from django.urls import reverse

from core import constants
from questions.factories import QuestionFactory
from questions.models import Question
from users import constants as user_constants
from users.factories import DEFAULT_PASSWORD, UserFactory


QUESTION_DETAIL_URLS = [
    "questions:detail_view",
    "questions:detail_edit",
    "questions:detail_quizs",
    "questions:detail_contributions",
    "questions:detail_stats",
    "questions:detail_history",
]
QUESTION_CREATE_FORM_DEFAULT = {
    "text": "Question 1",
    "type": constants.QUESTION_TYPE_QCM,
    "difficulty": constants.QUESTION_DIFFICULTY_EASY,
    "language": constants.LANGUAGE_FRENCH,
    "answer_option_a": "Réponse A",
    "answer_option_b": "Réponse B",
    "answer_correct": "a",
    "visibility": constants.VISIBILITY_PUBLIC,
}


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


class QuizDetailEditViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_contributor_1 = UserFactory()
        cls.user_contributor_2 = UserFactory()
        cls.user_super_contributor = UserFactory(roles=[user_constants.USER_ROLE_SUPER_CONTRIBUTOR])
        cls.user_admin = UserFactory(roles=[user_constants.USER_ROLE_ADMINISTRATOR])
        cls.question_1 = QuestionFactory(
            text="Question 1", author=cls.user_contributor_1, visibility=constants.VISIBILITY_PUBLIC
        )
        cls.question_2 = QuestionFactory(
            text="Question 2", author=cls.user_contributor_1, visibility=constants.VISIBILITY_PRIVATE
        )

    def test_author_or_super_contributor_can_edit_public_question(self):
        for user in [self.user_contributor_1, self.user_super_contributor, self.user_admin]:
            self.client.login(email=user.email, password=DEFAULT_PASSWORD)
            url = reverse("questions:detail_edit", args=[self.question_1.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, '<form id="question_edit_form" ')
        # other contributors can't edit
        self.client.login(email=self.user_contributor_2.email, password=DEFAULT_PASSWORD)
        url = reverse("questions:detail_edit", args=[self.question_1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, '<form id="question_edit_form" ')
        self.assertContains(response, "Vous n'avez pas les droits nécessaires")

    def test_only_author_can_edit_private_question(self):
        # author can edit
        self.client.login(email=self.user_contributor_1.email, password=DEFAULT_PASSWORD)
        url = reverse("questions:detail_edit", args=[self.question_2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form id="question_edit_form" ')
        # other contributors can't edit
        for user in [self.user_contributor_2, self.user_super_contributor, self.user_admin]:
            self.client.login(email=user.email, password=DEFAULT_PASSWORD)
            url = reverse("questions:detail_edit", args=[self.question_2.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertNotContains(response, '<form id="question_edit_form" ')
            self.assertContains(response, "Vous n'avez pas les droits nécessaires")


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
        response = self.client.post(url, data=QUESTION_CREATE_FORM_DEFAULT)
        self.assertEqual(response.status_code, 302)  # 201
        self.assertEqual(Question.objects.count(), 1)
