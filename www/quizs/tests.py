from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from activity.models import Event
from core import constants
from quizs.factories import QuizFactory
from quizs.models import Quiz
from users import constants as user_constants
from users.factories import DEFAULT_PASSWORD, UserFactory


QUIZ_DETAIL_URLS = [
    "quizs:detail_view",
    "quizs:detail_edit",
    "quizs:detail_questions",
    "quizs:detail_contributions",
    "quizs:detail_stats",
    "quizs:detail_history",
]

QUIZ_CREATE_FORM_DEFAULT = {
    "name": "Quiz 1",
    "language": constants.LANGUAGE_FRENCH,
    "visibility": constants.VISIBILITY_PUBLIC,
}


class QuizListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("quizs:list")
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()
        cls.quiz_1 = QuizFactory(name="Quiz 1")
        cls.quiz_2 = QuizFactory(name="Quiz 2")

    def test_only_contributor_can_access_quiz_list(self):
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
            self.assertIn("/accounts/login/?next=", response.url)

    def test_contributor_can_access_quiz_detail(self):
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        url = reverse("quizs:detail_view", args=[self.quiz_1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["quiz"].id, self.quiz_1.id)


class QuizDetailEditViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_contributor_1 = UserFactory()
        cls.user_contributor_2 = UserFactory()
        cls.user_admin = UserFactory(roles=[user_constants.USER_ROLE_ADMINISTRATOR])
        cls.quiz_1 = QuizFactory(
            name="Quiz 1",
            # authors=[cls.user_contributor_1],
            visibility=constants.VISIBILITY_PUBLIC,
            validation_status=constants.VALIDATION_STATUS_IN_PROGRESS,
            publish=False,
        )
        cls.quiz_1.authors.set([cls.user_contributor_1])
        cls.quiz_2 = QuizFactory(
            name="Quiz 2", visibility=constants.VISIBILITY_PRIVATE
        )  # authors=[cls.user_contributor_1]
        cls.quiz_2.authors.set([cls.user_contributor_1])

    def test_author_or_admin_can_edit_public_quiz(self):
        for user in [self.user_contributor_1, self.user_admin]:
            self.client.login(email=user.email, password=DEFAULT_PASSWORD)
            url = reverse("quizs:detail_edit", args=[self.quiz_1.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, '<form id="quiz_edit_form" ')
        # other contributors can't edit
        self.client.login(email=self.user_contributor_2.email, password=DEFAULT_PASSWORD)
        url = reverse("quizs:detail_edit", args=[self.quiz_1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, '<form id="quiz_edit_form" ')
        self.assertContains(response, "Vous n'avez pas les droits nécessaires")

    def test_administrator_can_validate_and_publish_public_quiz(self):
        self.client.login(email=self.user_admin.email, password=DEFAULT_PASSWORD)
        self.assertEqual(self.quiz_1.validation_status, constants.VALIDATION_STATUS_IN_PROGRESS)
        self.assertEqual(self.quiz_1.publish, False)
        url = reverse("quizs:detail_edit", args=[self.quiz_1.id])
        QUIZ_EDIT_FORM = {
            **QUIZ_CREATE_FORM_DEFAULT,
            "validation_status": constants.VALIDATION_STATUS_OK,
            "publish": True,
        }
        response = self.client.post(url, data=QUIZ_EDIT_FORM)
        self.assertEqual(response.status_code, 302)
        quiz = Quiz.objects.get(id=self.quiz_1.id)
        self.assertEqual(quiz.validator, self.user_admin)
        self.assertEqual(quiz.validation_date.date(), timezone.now().date())
        self.assertEqual(quiz.publish_date.date(), timezone.now().date())
        self.assertEqual(Event.objects.count(), 1 + 1)

    def test_only_author_can_edit_private_quiz(self):
        # author can edit
        self.client.login(email=self.user_contributor_1.email, password=DEFAULT_PASSWORD)
        url = reverse("quizs:detail_edit", args=[self.quiz_2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form id="quiz_edit_form" ')
        # other contributors can't edit
        for user in [self.user_contributor_2, self.user_admin]:
            self.client.login(email=user.email, password=DEFAULT_PASSWORD)
            url = reverse("quizs:detail_edit", args=[self.quiz_2.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertNotContains(response, '<form id="quiz_edit_form" ')
            self.assertContains(response, "Vous n'avez pas les droits nécessaires")


class QuizDetailQuestionListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_contributor_1 = UserFactory()
        cls.user_contributor_2 = UserFactory()
        cls.user_admin = UserFactory(roles=[user_constants.USER_ROLE_ADMINISTRATOR])
        cls.quiz_1 = QuizFactory(name="Quiz 1")  # authors=[cls.user_contributor_1]
        cls.quiz_1.authors.set([cls.user_contributor_1])

    def test_author_or_admin_can_edit_quiz_question_list(self):
        for user in [self.user_contributor_1, self.user_admin]:
            self.client.login(email=user.email, password=DEFAULT_PASSWORD)
            url = reverse("quizs:detail_questions", args=[self.quiz_1.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Modifier les questions")
            self.assertContains(response, '<form id="quiz_question_edit_form" ')
        # other contributors can't edit
        self.client.login(email=self.user_contributor_2.email, password=DEFAULT_PASSWORD)
        url = reverse("quizs:detail_questions", args=[self.quiz_1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Modifier les questions")
        self.assertNotContains(response, '<form id="quiz_question_edit_form" ')


class QuizCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("quizs:create")
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()

    def test_only_contributor_can_access_quiz_create(self):
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

    def test_contributor_can_create_quiz(self):
        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        response = self.client.post(self.url, data=QUIZ_CREATE_FORM_DEFAULT)
        self.assertEqual(response.status_code, 302)  # 201
        self.assertEqual(Quiz.objects.count(), 1)
        self.assertEqual(Event.objects.count(), 1)
        quiz = Quiz.objects.last()
        self.assertEqual(quiz.authors.count(), 1)
        self.assertEqual(quiz.authors.first(), self.user_contributor)
