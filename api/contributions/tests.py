from django.test import TestCase
from django.urls import reverse

from contributions.models import Comment
from core import constants
from questions.factories import QuestionFactory


class CommentApiTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.question = QuestionFactory()
        cls.comment_app = Comment.objects.create(type=constants.COMMENT_TYPE_COMMENT_APP)
        cls.comment_question_published = Comment.objects.create(
            type=constants.COMMENT_TYPE_COMMENT_APP, question=cls.question, publish=True
        )

    def test_comment_list(self):
        url = reverse("api:contribution-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data["results"], list)
        self.assertEqual(len(response.data["results"]), 1)


class CommentCreateApiTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.question = QuestionFactory()

    def test_comment_create(self):
        url = reverse("api:contribution-list")
        response = self.client.post(
            url,
            data={"text": "du texte", "description": "une description", "type": constants.COMMENT_TYPE_COMMENT_APP},
        )
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)
        # question comment
        response = self.client.post(
            url,
            data={
                "text": "du texte",
                "description": "une description",
                "type": constants.COMMENT_TYPE_COMMENT_QUESTION,
                "question": self.question.id,
            },
        )
        self.assertEqual(response.status_code, 201)
