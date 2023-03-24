from django.test import TestCase
from django.urls import reverse

from contributions.models import Comment
from core import constants
from questions.factories import QuestionFactory
from quizs.factories import QuizFactory


class CommentCreateApiTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("api:contribution-list")
        cls.question = QuestionFactory()
        cls.quiz = QuizFactory()

    def test_comment_create(self):
        response = self.client.post(
            self.url,
            data={"text": "du texte", "description": "une description", "type": constants.COMMENT_TYPE_COMMENT_APP},
        )
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(Comment.objects.last().status, constants.COMMENT_STATUS_NEW)

    def test_comment_question_create(self):
        response = self.client.post(
            self.url,
            data={
                "text": "du texte",
                "description": "une description",
                "type": constants.COMMENT_TYPE_COMMENT_QUESTION,
                "question": self.question.id,
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.last().question_id, self.question.id)

    def test_comment_quiz_create(self):
        response = self.client.post(
            self.url,
            data={
                "text": "du texte",
                "description": "une description",
                "type": constants.COMMENT_TYPE_COMMENT_QUIZ,
                "quiz": self.quiz.id,
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.last().quiz_id, self.quiz.id)
