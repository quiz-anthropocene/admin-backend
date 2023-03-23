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
        cls.comment_with_reply = CommentFactory(text="un commentaire", type=constants.COMMENT_TYPE_COMMENT_APP)
        cls.comment_reply = CommentFactory(type=constants.COMMENT_TYPE_REPLY, parent=cls.comment_with_reply)
        CommentFactory(type=constants.COMMENT_TYPE_COMMENT_QUESTION, question=cls.question)
        CommentFactory(type=constants.COMMENT_TYPE_COMMENT_QUIZ, quiz=cls.quiz)
        CommentFactory(type=constants.COMMENT_TYPE_ERROR_APP)

    def test_str(self):
        self.assertEqual(str(self.comment_with_reply), "un commentaire")

    def test_has_replies(self):
        self.assertTrue(self.comment_with_reply.has_replies)
        self.assertFalse(self.comment_reply.has_replies)


class CommentModelQuerySetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.question = QuestionFactory()
        cls.quiz = QuizFactory()
        cls.comment_with_reply_1 = CommentFactory(type=constants.COMMENT_TYPE_COMMENT_APP, publish=True)
        cls.comment_reply_reply_1 = CommentFactory(type=constants.COMMENT_TYPE_REPLY, parent=cls.comment_with_reply_1)
        cls.comment_reply_note_1 = CommentFactory(
            type=constants.COMMENT_TYPE_COMMENT_CONTRIBUTOR, parent=cls.comment_with_reply_1
        )
        cls.comment_with_reply_2 = CommentFactory(type=constants.COMMENT_TYPE_COMMENT_APP)
        cls.comment_reply_reply_2 = CommentFactory(type=constants.COMMENT_TYPE_REPLY, parent=cls.comment_with_reply_2)
        cls.comment_with_reply_3 = CommentFactory(type=constants.COMMENT_TYPE_COMMENT_APP)
        cls.comment_reply_note_3 = CommentFactory(
            type=constants.COMMENT_TYPE_COMMENT_CONTRIBUTOR, parent=cls.comment_with_reply_3
        )
        CommentFactory(type=constants.COMMENT_TYPE_COMMENT_QUESTION, question=cls.question)
        CommentFactory(type=constants.COMMENT_TYPE_COMMENT_QUIZ, quiz=cls.quiz)
        CommentFactory(type=constants.COMMENT_TYPE_ERROR_APP)

    def test_comment_count(self):
        self.assertEqual(Comment.objects.count(), 10)

    def test_comment_exclude_replies(self):
        self.assertEqual(Comment.objects.exclude_replies().count(), 10 - 2)

    def test_comment_exclude_contributor_comments(self):
        self.assertEqual(Comment.objects.exclude_contributor_comments().count(), 10 - 2)

    def test_comment_exclude_contributor_work(self):
        self.assertEqual(Comment.objects.exclude_contributor_work().count(), 10 - 4)

    def test_comment_exclude_errors(self):
        self.assertEqual(Comment.objects.exclude_errors().count(), 10 - 1)

    def test_comment_only_replies(self):
        self.assertEqual(Comment.objects.only_replies().count(), 2)

    def test_comment_only_notes(self):
        self.assertEqual(Comment.objects.only_notes().count(), 2)

    def test_comment_has_replies_contributor_comments(self):
        self.assertEqual(Comment.objects.has_replies_contributor_comments().count(), 2)

    def test_comment_has_replies_reply(self):
        self.assertEqual(Comment.objects.has_replies_reply().count(), 2)

    def test_comment_has_replies_contributor_work(self):
        self.assertEqual(Comment.objects.has_replies_contributor_work().count(), 3)

    def test_comment_has_parent(self):
        self.assertEqual(Comment.objects.has_parent().count(), 4)

    def test_comment_published(self):
        self.assertEqual(Comment.objects.published().count(), 1)
