import time

from django.core import management
from django.test import TestCase

from api.models import (
    Question,
    # QuestionAggStat,
    QuestionAnswerEvent,
    QuestionFeedbackEvent,
)
from api.tests.factories import QuestionFactory


class CleanupQuestionStatsCommandTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # question_1
        cls.question_1 = QuestionFactory(answer_correct="a")
        cls.question_1.agg_stats.answer_count = 1
        cls.question_1.agg_stats.answer_success_count = 2
        cls.question_1.agg_stats.like_count = 3
        cls.question_1.agg_stats.dislike_count = 4
        cls.question_1.agg_stats.save()
        QuestionAnswerEvent.objects.create(
            question_id=cls.question_1.id, choice="a", source="question"
        )
        QuestionAnswerEvent.objects.create(
            question_id=cls.question_1.id, choice="b", source="question"
        )
        QuestionAnswerEvent.objects.create(
            question_id=cls.question_1.id, choice="c", source="quiz"
        )
        QuestionFeedbackEvent.objects.create(
            question_id=cls.question_1.id, choice="like", source="question"
        )
        QuestionFeedbackEvent.objects.create(
            question_id=cls.question_1.id, choice="dislike", source="question"
        )
        QuestionFeedbackEvent.objects.create(
            question_id=cls.question_1.id, choice="like", source="quiz"
        )
        # question_2
        cls.question_2 = QuestionFactory(answer_correct="b")
        cls.question_2.agg_stats.answer_count = 1
        cls.question_2.agg_stats.save()
        QuestionAnswerEvent.objects.create(
            question_id=cls.question_2.id, choice="a", source="question"
        )
        QuestionFeedbackEvent.objects.create(
            question_id=cls.question_2.id, choice="like", source="quiz"
        )

    def test_question_updates(self):
        self.assertEqual(QuestionAnswerEvent.objects.count(), 3 + 1)
        self.assertEqual(QuestionFeedbackEvent.objects.count(), 3 + 1)

        management.call_command(
            "reset_question_stats", self.question_1.id, "--no-input"
        )

        time.sleep(2)

        question_1_updated = Question.objects.get(pk=self.question_1.id)

        # question answer stats
        self.assertEqual(question_1_updated.agg_stats.answer_count, 0)
        self.assertEqual(question_1_updated.agg_stats.answer_success_count, 0)
        self.assertEqual(
            QuestionAnswerEvent.objects.for_question(
                question_id=self.question_1.id
            ).count(),
            0,
        )

        # question feedback stats
        self.assertEqual(question_1_updated.agg_stats.like_count, 0)
        self.assertEqual(question_1_updated.agg_stats.dislike_count, 0)
        self.assertEqual(
            QuestionFeedbackEvent.objects.for_question(
                question_id=self.question_1.id
            ).count(),
            0,
        )

        # check that there were no impact on question_2
        self.assertEqual(self.question_2.agg_stats.answer_count, 1)
        self.assertEqual(
            QuestionAnswerEvent.objects.for_question(
                question_id=self.question_2.id
            ).count(),
            1,
        )
        self.assertEqual(
            QuestionFeedbackEvent.objects.for_question(
                question_id=self.question_2.id
            ).count(),
            1,
        )
