from django.test import TestCase

from contributions.factories import ContributionFactory
from contributions.models import Contribution
from core import constants
from questions.factories import QuestionFactory
from quizs.factories import QuizFactory


class ContributionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.question = QuestionFactory()
        cls.quiz = QuizFactory()
        cls.contribution_with_reply = ContributionFactory(
            text="un commentaire", type=constants.CONTRIBUTION_TYPE_COMMENT_APP
        )
        cls.contribution_reply = ContributionFactory(
            type=constants.CONTRIBUTION_TYPE_REPLY, parent=cls.contribution_with_reply
        )
        ContributionFactory(type=constants.CONTRIBUTION_TYPE_COMMENT_QUESTION, question=cls.question)
        ContributionFactory(type=constants.CONTRIBUTION_TYPE_COMMENT_QUIZ, quiz=cls.quiz)
        ContributionFactory(type=constants.CONTRIBUTION_TYPE_ERROR_APP)

    def test_str(self):
        self.assertEqual(str(self.contribution_with_reply), "un commentaire")

    def test_has_replies(self):
        self.assertTrue(self.contribution_with_reply.has_replies)
        self.assertFalse(self.contribution_reply.has_replies)


class ContributionModelQuerySetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.question = QuestionFactory()
        cls.quiz = QuizFactory()
        cls.contribution_with_reply = ContributionFactory(type=constants.CONTRIBUTION_TYPE_COMMENT_APP)
        cls.contribution_reply = ContributionFactory(
            type=constants.CONTRIBUTION_TYPE_REPLY, parent=cls.contribution_with_reply
        )
        ContributionFactory(type=constants.CONTRIBUTION_TYPE_COMMENT_QUESTION, question=cls.question)
        ContributionFactory(type=constants.CONTRIBUTION_TYPE_COMMENT_QUIZ, quiz=cls.quiz)
        ContributionFactory(type=constants.CONTRIBUTION_TYPE_ERROR_APP)

    def test_contributions_exclude_replies(self):
        self.assertEqual(Contribution.objects.exclude_replies().count(), 4)

    def test_contributions_exclude_errors(self):
        self.assertEqual(Contribution.objects.exclude_errors().count(), 4)
