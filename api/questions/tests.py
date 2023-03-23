from django.test import TestCase
from django.urls import reverse

from contributions.models import Comment
from core import constants
from questions.factories import QuestionFactory


class QuestionApiTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.question_public = QuestionFactory(
            visibility=constants.VISIBILITY_PUBLIC, validation_status=constants.VALIDATION_STATUS_TO_VALIDATE
        )
        cls.question_public_validated = QuestionFactory(
            visibility=constants.VISIBILITY_PUBLIC, validation_status=constants.VALIDATION_STATUS_VALIDATED
        )
        cls.question_private = QuestionFactory(
            visibility=constants.VISIBILITY_PRIVATE, validation_status=constants.VALIDATION_STATUS_TO_VALIDATE
        )
        cls.question_private_validated = QuestionFactory(
            visibility=constants.VISIBILITY_PRIVATE, validation_status=constants.VALIDATION_STATUS_VALIDATED
        )

    def test_question_list(self):
        url = reverse("api:question-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data["results"], list)
        self.assertEqual(len(response.data["results"]), 1)

    def test_question_detail(self):
        # works if the question is public & validated
        url = reverse("api:question-detail", args=[self.question_public_validated.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        # doesn't work if the question is not validated or not public
        for question in [self.question_public, self.question_private, self.question_private_validated]:
            url = reverse("api:question-detail", args=[question.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)


class QuestionCommentApiTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.question_public = QuestionFactory(
            visibility=constants.VISIBILITY_PUBLIC, validation_status=constants.VALIDATION_STATUS_TO_VALIDATE
        )
        cls.question_public_validated = QuestionFactory(
            visibility=constants.VISIBILITY_PUBLIC, validation_status=constants.VALIDATION_STATUS_VALIDATED
        )
        cls.question_private = QuestionFactory(
            visibility=constants.VISIBILITY_PRIVATE, validation_status=constants.VALIDATION_STATUS_TO_VALIDATE
        )
        cls.question_private_validated = QuestionFactory(
            visibility=constants.VISIBILITY_PRIVATE, validation_status=constants.VALIDATION_STATUS_VALIDATED
        )
        cls.comment_question_public = Comment.objects.create(
            type=constants.COMMENT_TYPE_COMMENT_QUESTION, question=cls.question_public, publish=True
        )
        cls.comment_question_public_validated_1 = Comment.objects.create(
            type=constants.COMMENT_TYPE_COMMENT_QUESTION, question=cls.question_public_validated, publish=False
        )
        cls.comment_question_public_validated_2 = Comment.objects.create(
            type=constants.COMMENT_TYPE_COMMENT_QUESTION, question=cls.question_public_validated, publish=True
        )
        cls.comment_question_private = Comment.objects.create(
            type=constants.COMMENT_TYPE_COMMENT_QUESTION, question=cls.question_private, publish=True
        )
        cls.comment_question_private_validated = Comment.objects.create(
            type=constants.COMMENT_TYPE_COMMENT_QUESTION, question=cls.question_private_validated, publish=True
        )

    def test_question_comment_list(self):
        # works if the question is public & validated + the comment is published
        url = reverse("api:question-contributions", args=[self.question_public_validated.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data["results"], list)
        self.assertEqual(len(response.data["results"]), 1)
        # doesn't work if the question is not validated or not public
        for question in [self.question_public, self.question_private, self.question_private_validated]:
            url = reverse("api:question-contributions", args=[question.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)
