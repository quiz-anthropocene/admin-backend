from django.test import TestCase
from django.urls import reverse

from core import constants
from questions.factories import QuestionFactory


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
