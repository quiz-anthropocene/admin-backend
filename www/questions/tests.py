import json

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from activity.models import Event
from core import constants
from questions.factories import QuestionFactory
from questions.models import Question
from users import constants as user_constants
from users.factories import DEFAULT_PASSWORD, UserFactory


QUESTION_DETAIL_URLS = [
    "questions:detail_view",
    "questions:detail_edit",
    "questions:detail_quizs",
    "questions:detail_comments",
    "questions:detail_stats",
    "questions:detail_history",
]
QUESTION_CREATE_FORM_DEFAULT = {
    "text": "Question 1",
    "type": constants.QUESTION_TYPE_QCM,
    "difficulty": constants.QUESTION_DIFFICULTY_EASY,
    "language": constants.LANGUAGE_FRENCH,
    "answer_choice_a": "Réponse A",
    "answer_choice_b": "Réponse B",
    "answer_correct": "a",
    "visibility": constants.VISIBILITY_PUBLIC,
}


class QuestionListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("questions:list")
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()
        cls.question_1 = QuestionFactory()
        cls.question_2 = QuestionFactory()

    def test_only_contributor_can_access_question_list(self):
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
        self.assertEqual(len(response.context["questions"]), 2)


class QuestionDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.question_1 = QuestionFactory()
        cls.question_2 = QuestionFactory()

    def test_anonymous_user_cannot_access_question_detail(self):
        for detail_url in QUESTION_DETAIL_URLS:
            url = reverse(detail_url, args=[self.question_1.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn("/accounts/login/?next=", response.url)

    def test_contributor_can_access_question_detail(self):
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        for detail_url in QUESTION_DETAIL_URLS:
            url = reverse(detail_url, args=[self.question_1.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["question"].id, self.question_1.id)


class QuestionDetailEditViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_contributor_1 = UserFactory()
        cls.user_contributor_2 = UserFactory()
        cls.user_super_contributor = UserFactory(roles=[user_constants.USER_ROLE_SUPER_CONTRIBUTOR])
        cls.user_admin = UserFactory(roles=[user_constants.USER_ROLE_ADMINISTRATOR])
        cls.question_1 = QuestionFactory(
            text="Question 1",
            author=cls.user_contributor_1,
            visibility=constants.VISIBILITY_PUBLIC,
            validation_status=constants.VALIDATION_STATUS_TO_VALIDATE,
        )
        cls.question_2 = QuestionFactory(
            text="Question 2", author=cls.user_contributor_1, visibility=constants.VISIBILITY_PRIVATE
        )

    def test_only_author_or_super_contributor_can_edit_public_question(self):
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
        self.assertContains(response, " pas les droits ")

    def test_administrator_can_validate_public_question(self):
        self.client.login(email=self.user_admin.email, password=DEFAULT_PASSWORD)
        self.assertEqual(self.question_1.validation_status, constants.VALIDATION_STATUS_TO_VALIDATE)
        url = reverse("questions:detail_edit", args=[self.question_1.id])
        QUESTION_EDIT_FORM = {
            **QUESTION_CREATE_FORM_DEFAULT,
            "text": self.question_1.text,
            "category": self.question_1.category.id,
            "author": self.question_1.author,
            "visibility": self.question_1.visibility,
            "validation_status": constants.VALIDATION_STATUS_VALIDATED,
        }
        response = self.client.post(url, data=QUESTION_EDIT_FORM)
        self.assertEqual(response.status_code, 302)
        question = Question.objects.get(id=self.question_1.id)
        self.assertEqual(question.validator, self.user_admin)
        self.assertEqual(question.validation_date.date(), timezone.now().date())
        self.assertEqual(Event.objects.count(), 1)

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
            self.assertContains(response, " pas les droits ")


class QuestionCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("questions:create")
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()

    def test_only_contributor_can_access_question_create(self):
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

    def test_contributor_can_create_question(self):
        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        response = self.client.post(self.url, data=QUESTION_CREATE_FORM_DEFAULT)
        self.assertEqual(response.status_code, 302)  # 201
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Event.objects.count(), 1)
        question = Question.objects.last()
        self.assertEqual(question.author, self.user_contributor)


class QuestionAutocompleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("questions:search")
        cls.user = UserFactory(roles=[])
        cls.user_contributor_1 = UserFactory()
        cls.user_contributor_2 = UserFactory()
        cls.question_1 = QuestionFactory(text="Test", author=cls.user_contributor_1)

    def test_only_contributor_can_access_question_autocomplete(self):
        # anonymous
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/?next=", response.url)
        # simple user
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        # self.assertEqual(response.url, "/")  # redirected to home
        self.assertNotIn("/questions/search/", response.url)
        # contributor
        self.client.login(email=self.user_contributor_1.email, password=DEFAULT_PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_contributor_can_search_question_by_id_or_text(self):
        self.client.login(email=self.user_contributor_1.email, password=DEFAULT_PASSWORD)
        # search by id
        response = self.client.get(self.url, {"q": str(self.question_1.id)})
        response_data = json.loads(response.content.decode("utf8"))
        self.assertEqual(len(response_data["results"]), 1)
        # search by text
        response = self.client.get(self.url, {"q": "test"})
        response_data = json.loads(response.content.decode("utf8"))
        self.assertEqual(len(response_data["results"]), 1)

    def test_should_not_return_private_questions_except_if_author(self):
        QuestionFactory(text="Another test", author=self.user_contributor_2, visibility=constants.VISIBILITY_PRIVATE)
        # other contributor
        self.client.login(email=self.user_contributor_1.email, password=DEFAULT_PASSWORD)
        response = self.client.get(self.url, {"q": "another"})
        response_data = json.loads(response.content.decode("utf8"))
        self.assertEqual(len(response_data["results"]), 0)
        # author
        self.client.login(email=self.user_contributor_2.email, password=DEFAULT_PASSWORD)
        response = self.client.get(self.url, {"q": "another"})
        response_data = json.loads(response.content.decode("utf8"))
        self.assertEqual(len(response_data["results"]), 1)
