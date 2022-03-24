import time

from django.core import management
from django.test import TestCase

from api.tests.factories import QuizFactory
from stats.models import QuizAnswerEvent, QuizFeedbackEvent


class CleanupQuizStatsCommandTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # quiz_1
        cls.quiz_1 = QuizFactory(name="quiz 1")
        QuizAnswerEvent.objects.create(quiz_id=cls.quiz_1.id, answer_success_count=1)
        QuizAnswerEvent.objects.create(quiz_id=cls.quiz_1.id, answer_success_count=2)
        QuizAnswerEvent.objects.create(quiz_id=cls.quiz_1.id, answer_success_count=3)
        QuizFeedbackEvent.objects.create(quiz_id=cls.quiz_1.id, choice="like")
        QuizFeedbackEvent.objects.create(quiz_id=cls.quiz_1.id, choice="dislike")
        QuizFeedbackEvent.objects.create(quiz_id=cls.quiz_1.id, choice="like")
        # quiz_2
        cls.quiz_2 = QuizFactory(name="quiz 2")
        QuizAnswerEvent.objects.create(quiz_id=cls.quiz_2.id, answer_success_count=1)
        QuizFeedbackEvent.objects.create(quiz_id=cls.quiz_2.id, choice="like")

    def test_quiz_updates(self):
        self.assertEqual(QuizAnswerEvent.objects.count(), 3 + 1)
        self.assertEqual(QuizFeedbackEvent.objects.count(), 3 + 1)

        management.call_command("reset_quiz_stats", self.quiz_1.id, "--no-input")

        time.sleep(2)

        # quiz_1_updated = Quiz.objects.get(pk=self.quiz_1.id)

        # quiz answer stats
        self.assertEqual(QuizAnswerEvent.objects.for_quiz(quiz_id=self.quiz_1.id).count(), 0)

        # quiz feedback stats
        self.assertEqual(QuizFeedbackEvent.objects.for_quiz(quiz_id=self.quiz_1.id).count(), 0)

        # check that there were no impact on quiz_2
        self.assertEqual(QuizAnswerEvent.objects.for_quiz(quiz_id=self.quiz_2.id).count(), 1)
        self.assertEqual(QuizFeedbackEvent.objects.for_quiz(quiz_id=self.quiz_2.id).count(), 1)
