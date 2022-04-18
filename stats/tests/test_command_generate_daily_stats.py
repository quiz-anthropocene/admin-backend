from datetime import datetime

from django.core import management
from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time

from core.models import Configuration
from questions.factories import QuestionFactory
from questions.models import Question
from quizs.factories import QuizFactory
from quizs.models import Quiz
from stats import constants
from stats.models import DailyStat, QuestionAnswerEvent, QuestionFeedbackEvent, QuizAnswerEvent


class CleanupAppStatsCommandTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Configuration.objects.create(daily_stat_last_aggregated=timezone.make_aware(datetime(2020, 4, 30)))
        cls.question_1 = QuestionFactory(answer_correct="a")
        cls.question_1.agg_stats.answer_count = 2
        cls.question_1.agg_stats.save()
        QuestionAnswerEvent.objects.create(question_id=cls.question_1.id, choice="a", source="question")
        QuestionAnswerEvent.objects.create(question_id=cls.question_1.id, choice="b", source="question")
        QuestionAnswerEvent.objects.create(question_id=cls.question_1.id, choice="c", source="quiz")
        QuestionFeedbackEvent.objects.create(question_id=cls.question_1.id, choice="like", source="question")
        QuestionFeedbackEvent.objects.create(question_id=cls.question_1.id, choice="dislike", source="question")
        QuestionFeedbackEvent.objects.create(question_id=cls.question_1.id, choice="like", source="quiz")
        cls.quiz_1 = QuizFactory(name="quiz 1")
        QuizAnswerEvent.objects.create(quiz_id=cls.quiz_1.id, answer_success_count=1)
        DailyStat.objects.create(
            date="2020-04-30",
            question_answer_count=10,
            question_feedback_count=5,
            quiz_answer_count=2,
            hour_split=constants.DEFAULT_DAILY_STAT_HOUR_SPLIT,
        )
        with freeze_time("2020-04-30 12:30:00"):
            QuestionAnswerEvent.objects.create(question_id=cls.question_1.id, choice="a", source="question")
            QuestionAnswerEvent.objects.create(question_id=cls.question_1.id, choice="b", source="question")
            QuestionAnswerEvent.objects.create(question_id=cls.question_1.id, choice="c", source="quiz")
            QuestionFeedbackEvent.objects.create(question_id=cls.question_1.id, choice="like", source="question")
            QuestionFeedbackEvent.objects.create(question_id=cls.question_1.id, choice="dislike", source="question")
            QuestionFeedbackEvent.objects.create(question_id=cls.question_1.id, choice="like", source="quiz")
            QuizAnswerEvent.objects.create(quiz_id=cls.quiz_1.id, answer_success_count=1)

    def test_question_updates(self):
        self.assertEqual(QuestionAnswerEvent.objects.count(), 6)
        self.assertEqual(QuestionFeedbackEvent.objects.count(), 6)
        self.assertEqual(QuizAnswerEvent.objects.count(), 2)

        management.call_command("generate_daily_stats")

        question_1_updated = Question.objects.get(pk=self.question_1.id)
        quiz_1_updated = Quiz.objects.get(pk=self.quiz_1.id)
        daily_stat_today = DailyStat.objects.get(date=datetime.utcnow().date())
        daily_stat_freeze_time = DailyStat.objects.get(date="2020-04-30")

        # question answer stats
        self.assertEqual(question_1_updated.agg_stats.answer_count, 2 + 6)
        self.assertEqual(question_1_updated.agg_stats.answer_success_count, 2)
        self.assertEqual(QuestionAnswerEvent.objects.count(), 6)

        # question feedback stats
        self.assertEqual(question_1_updated.agg_stats.like_count, 4)
        self.assertEqual(question_1_updated.agg_stats.dislike_count, 2)
        self.assertEqual(QuestionFeedbackEvent.objects.count(), 6)

        # quiz answer stats
        self.assertEqual(quiz_1_updated.stats.count(), 2)
        self.assertEqual(QuizAnswerEvent.objects.count(), 2)

        # daily stats today
        self.assertEqual(daily_stat_today.question_answer_count, 3)
        self.assertEqual(daily_stat_today.question_answer_from_quiz_count, 1)
        self.assertEqual(daily_stat_today.quiz_answer_count, 1)
        self.assertEqual(
            daily_stat_today.hour_split[str(datetime.utcnow().hour)]["question_answer_count"],
            3,
        )
        self.assertEqual(
            daily_stat_today.hour_split[str(datetime.utcnow().hour)]["question_answer_from_quiz_count"],
            1,
        )
        self.assertEqual(daily_stat_today.question_feedback_count, 3)
        self.assertEqual(daily_stat_today.question_feedback_from_quiz_count, 1)
        self.assertEqual(
            daily_stat_today.hour_split[str(datetime.utcnow().hour)]["question_feedback_count"],
            3,
        )
        self.assertEqual(
            daily_stat_today.hour_split[str(datetime.utcnow().hour)]["question_feedback_from_quiz_count"],
            1,
        )
        self.assertEqual(
            daily_stat_today.hour_split[str(datetime.utcnow().hour)]["quiz_answer_count"],
            1,
        )

        # daily stats freeze time
        self.assertEqual(daily_stat_freeze_time.question_answer_count, 10 + 3)
        self.assertEqual(daily_stat_freeze_time.question_feedback_count, 5 + 3)
        self.assertEqual(daily_stat_freeze_time.quiz_answer_count, 2 + 1)
