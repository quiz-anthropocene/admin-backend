from datetime import datetime

from freezegun import freeze_time

from django.core import management
from django.test import TestCase

from api import constants
from api.models import Question, QuestionStat, QuestionFeedback, DailyStat


class CleanupQuestionStatsCommandTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.question_1 = Question.objects.create(answer_correct="a")
        cls.question_2 = Question.objects.create(answer_correct="b")
        QuestionStat.objects.create(
            question_id=cls.question_1.id, choice="a", source="question"
        )
        QuestionStat.objects.create(
            question_id=cls.question_1.id, choice="b", source="question"
        )
        QuestionStat.objects.create(
            question_id=cls.question_1.id, choice="c", source="quiz"
        )
        QuestionFeedback.objects.create(
            question_id=cls.question_1.id, choice="like", source="question"
        )
        QuestionFeedback.objects.create(
            question_id=cls.question_1.id, choice="dislike", source="question"
        )
        QuestionFeedback.objects.create(
            question_id=cls.question_1.id, choice="like", source="quiz"
        )
        DailyStat.objects.create(
            date="2020-04-30",
            question_answer_count=10,
            question_feedback_count=5,
            hour_split=constants.DEFAULT_DAILY_STAT_HOUR_SPLIT,
        )
        with freeze_time("2020-04-30 12:30:00"):
            QuestionStat.objects.create(
                question_id=cls.question_1.id, choice="a", source="question"
            )
            QuestionStat.objects.create(
                question_id=cls.question_1.id, choice="b", source="question"
            )
            QuestionStat.objects.create(
                question_id=cls.question_1.id, choice="c", source="quiz"
            )
            QuestionFeedback.objects.create(
                question_id=cls.question_1.id, choice="like", source="question"
            )
            QuestionFeedback.objects.create(
                question_id=cls.question_1.id, choice="dislike", source="question"
            )
            QuestionFeedback.objects.create(
                question_id=cls.question_1.id, choice="like", source="quiz"
            )

    def test_question_updates(self):
        self.assertEqual(QuestionStat.objects.count(), 6)
        self.assertEqual(QuestionFeedback.objects.count(), 6)

        management.call_command("cleanup_question_stats")

        question_1_updated = Question.objects.get(pk=self.question_1.id)
        daily_stat_today = DailyStat.objects.get(date=datetime.utcnow().date())
        daily_stat_freeze_time = DailyStat.objects.get(date="2020-04-30")

        # question answer stats
        self.assertEqual(question_1_updated.answer_count, 6)
        self.assertEqual(question_1_updated.answer_success_count, 2)
        self.assertEqual(QuestionStat.objects.count(), 0)

        # question feedback stats
        self.assertEqual(question_1_updated.like_count, 4)
        self.assertEqual(question_1_updated.dislike_count, 2)
        self.assertEqual(QuestionFeedback.objects.count(), 0)

        # daily stats today
        self.assertEqual(daily_stat_today.question_answer_count, 3)
        self.assertEqual(daily_stat_today.question_answer_from_quiz_count, 1)
        self.assertEqual(
            daily_stat_today.hour_split[str(datetime.utcnow().hour)][
                "question_answer_count"
            ],
            3,
        )
        self.assertEqual(
            daily_stat_today.hour_split[str(datetime.utcnow().hour)][
                "question_answer_from_quiz_count"
            ],
            1,
        )
        self.assertEqual(daily_stat_today.question_feedback_count, 3)
        self.assertEqual(daily_stat_today.question_feedback_from_quiz_count, 1)
        self.assertEqual(
            daily_stat_today.hour_split[str(datetime.utcnow().hour)][
                "question_feedback_count"
            ],
            3,
        )
        self.assertEqual(
            daily_stat_today.hour_split[str(datetime.utcnow().hour)][
                "question_feedback_from_quiz_count"
            ],
            1,
        )

        # daily stats freeze time
        self.assertEqual(daily_stat_freeze_time.question_answer_count, 13)
        self.assertEqual(daily_stat_freeze_time.question_feedback_count, 8)
