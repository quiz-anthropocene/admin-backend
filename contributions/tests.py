from django.test import TestCase

from contributions.factories import CommentFactory
from contributions.models import Comment
from core import constants
from questions.factories import QuestionFactory
from quizs.factories import QuizFactory


class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.question = QuestionFactory()
        cls.quiz = QuizFactory()
        cls.contribution_with_reply = CommentFactory(text="un commentaire", type=constants.COMMENT_TYPE_COMMENT_APP)
        cls.contribution_reply = CommentFactory(type=constants.COMMENT_TYPE_REPLY, parent=cls.contribution_with_reply)
        CommentFactory(type=constants.COMMENT_TYPE_COMMENT_QUESTION, question=cls.question)
        CommentFactory(type=constants.COMMENT_TYPE_COMMENT_QUIZ, quiz=cls.quiz)
        CommentFactory(type=constants.COMMENT_TYPE_ERROR_APP)

    def test_str(self):
        self.assertEqual(str(self.contribution_with_reply), "un commentaire")

    def test_has_replies(self):
        self.assertTrue(self.contribution_with_reply.has_replies)
        self.assertFalse(self.contribution_reply.has_replies)


class CommentModelQuerySetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.question = QuestionFactory()
        cls.quiz = QuizFactory()
        cls.contribution_with_reply = CommentFactory(type=constants.COMMENT_TYPE_COMMENT_APP)
        cls.contribution_reply = CommentFactory(type=constants.COMMENT_TYPE_REPLY, parent=cls.contribution_with_reply)
        cls.contribution_reply = CommentFactory(
            type=constants.COMMENT_TYPE_COMMENT_CONTRIBUTOR, parent=cls.contribution_with_reply
        )
        CommentFactory(type=constants.COMMENT_TYPE_COMMENT_QUESTION, question=cls.question)
        CommentFactory(type=constants.COMMENT_TYPE_COMMENT_QUIZ, quiz=cls.quiz)
        CommentFactory(type=constants.COMMENT_TYPE_ERROR_APP)

    def test_contributions_count(self):
        self.assertEqual(Comment.objects.count(), 6)

    def test_contributions_exclude_replies(self):
        self.assertEqual(Comment.objects.exclude_replies().count(), 6 - 1)

    def test_contributions_exclude_contributor_comments(self):
        self.assertEqual(Comment.objects.exclude_contributor_comments().count(), 6 - 1)

    def test_contributions_exclude_contributor_work(self):
        self.assertEqual(Comment.objects.exclude_contributor_work().count(), 6 - 2)

    def test_contributions_exclude_errors(self):
        self.assertEqual(Comment.objects.exclude_errors().count(), 6 - 1)
