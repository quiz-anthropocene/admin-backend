from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from core import constants
from questions.factories import QuestionFactory
from questions.models import Question
from quizs.factories import QuizFactory
from quizs.models import QuizQuestion
from stats.models import (
    DailyStat,
    QuestionAggStat,
    QuestionAnswerEvent,
    QuestionFeedbackEvent,
    QuizAnswerEvent,
    QuizFeedbackEvent,
)


datetime_50_days_ago = timezone.now() - timedelta(days=50)


class QuestionStatTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.question_1 = QuestionFactory(answer_correct="a")
        cls.question_1.agg_stats.answer_count = 5
        cls.question_1.agg_stats.answer_success_count = 2
        cls.question_1.agg_stats.like_count = 2
        cls.question_1.agg_stats.save()
        QuestionAnswerEvent.objects.create(question_id=cls.question_1.id, choice="a", source="question")
        QuestionFeedbackEvent.objects.create(question_id=cls.question_1.id, choice="dislike", source="quiz")
        cls.question_rm_1 = QuestionFactory(type=constants.QUESTION_TYPE_QCM_RM, answer_correct="ab")
        cls.question_rm_2 = QuestionFactory(type=constants.QUESTION_TYPE_QCM_RM, answer_correct="abc")
        cls.question_rm_3 = QuestionFactory(type=constants.QUESTION_TYPE_QCM_RM, answer_correct="abcd")
        QuestionAnswerEvent.objects.create(
            question_id=cls.question_rm_1.id, choice="cd", source="question", created=datetime_50_days_ago
        )
        cls.question_vf = QuestionFactory(type=constants.QUESTION_TYPE_VF, answer_correct="b")

    def test_question_answer_event_agg_count(self):
        self.assertEqual(QuestionAnswerEvent.objects.count(), 2)
        self.assertEqual(QuestionAnswerEvent.objects.agg_count(), 2)
        self.assertEqual(QuestionAnswerEvent.objects.agg_count("last_30_days"), 1)

    def test_question_agg_stat_created(self):
        self.assertEqual(Question.objects.count(), 1 + 3 + 1)
        self.assertEqual(QuestionAggStat.objects.count(), 1 + 3 + 1)
        question_agg_stat = QuestionAggStat.objects.first()
        self.assertEqual(question_agg_stat.question_id, self.question_1.id)

    def test_answer_count(self):
        self.assertEqual(self.question_1.answer_count_agg, 6)
        self.assertEqual(self.question_1.answer_success_count_agg, 3)
        self.assertEqual(self.question_1.answer_success_rate, 50)

    def test_feedback_count(self):
        self.assertEqual(self.question_1.like_count_agg, 2)
        self.assertEqual(self.question_1.dislike_count_agg, 1)


class QuizStatTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.question_1 = QuestionFactory(answer_correct="a")
        cls.quiz_1 = QuizFactory(name="quiz 1")  # questions=[cls.question_1.id]
        QuizQuestion.objects.create(quiz=cls.quiz_1, question=cls.question_1)
        QuestionAnswerEvent.objects.create(question_id=cls.question_1.id, choice="a", source="question")
        QuizAnswerEvent.objects.create(quiz_id=cls.quiz_1.id, answer_success_count=1, created=datetime_50_days_ago)
        QuizFeedbackEvent.objects.create(quiz_id=cls.quiz_1.id, choice="dislike")

    def test_quiz_answer_event_agg_count(self):
        self.assertEqual(QuizAnswerEvent.objects.count(), 1)
        self.assertEqual(QuizAnswerEvent.objects.agg_count(), 1)
        self.assertEqual(QuizAnswerEvent.objects.agg_count("last_30_days"), 0)

    def test_answer_count(self):
        self.assertEqual(self.quiz_1.answer_count_agg, 1)

    def test_feedback_count(self):
        self.assertEqual(self.quiz_1.like_count_agg, 0)
        self.assertEqual(self.quiz_1.dislike_count_agg, 1)


class DailyStatModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.question_1 = QuestionFactory(answer_correct="a")
        QuestionAnswerEvent.objects.create(question_id=cls.question_1.id, choice="a", source="question")
        # 3 daily stats in the same week
        DailyStat.objects.create(date="2020-04-30", question_answer_count=10, question_feedback_count=5)
        DailyStat.objects.create(date="2020-05-01", question_answer_count=2, question_feedback_count=1)
        DailyStat.objects.create(date="2020-05-02", question_answer_count=4, question_feedback_count=2)
        # 1 daily stats in the next week
        DailyStat.objects.create(date="2020-05-06", question_answer_count=1, question_feedback_count=1)
        # 1 daily stats in the next year
        DailyStat.objects.create(date="2021-05-01", question_answer_count=3, question_feedback_count=3)

    def test_question_answer_count_count(self):
        self.assertEqual(DailyStat.objects.agg_count("question_answer_count"), 20)
        self.assertEqual(DailyStat.objects.agg_count("question_feedback_count"), 12)
        self.assertEqual(DailyStat.objects.agg_count("quiz_answer_count"), 0)
        self.assertEqual(
            DailyStat.objects.agg_count("question_answer_count", since="week", week_or_month_iso_number=18),
            16,
        )
        self.assertEqual(
            DailyStat.objects.agg_count("question_answer_count", since="month", week_or_month_iso_number=4),
            10,
        )
        self.assertEqual(
            DailyStat.objects.agg_count("question_feedback_count", since="month", week_or_month_iso_number=5),
            4 + 3,
        )
        self.assertEqual(
            DailyStat.objects.agg_count(
                "question_feedback_count", since="month", week_or_month_iso_number=5, year=2020
            ),
            4,
        )
        agg_timeseries_per_day_1 = DailyStat.objects.agg_timeseries(field="question_answer_count", scale="day")
        self.assertEqual(len(agg_timeseries_per_day_1), 5)
        self.assertEqual(agg_timeseries_per_day_1[0]["day"], "2020-04-30")
        agg_timeseries_per_day_2 = DailyStat.objects.agg_timeseries(
            field="question_answer_count", scale="day", since_date="2020-05-02"
        )
        self.assertEqual(len(agg_timeseries_per_day_2), 3)
        self.assertEqual(agg_timeseries_per_day_2[0]["day"], "2020-05-02")
        agg_timeseries_per_month = DailyStat.objects.agg_timeseries(field="question_answer_count", scale="month")
        self.assertEqual(len(agg_timeseries_per_month), 3)
        self.assertEqual(agg_timeseries_per_month[0]["day"], "2020-04-01")
        self.assertEqual(agg_timeseries_per_month[0]["y"], 10)
        self.assertEqual(agg_timeseries_per_month[1]["day"], "2020-05-01")
        self.assertEqual(agg_timeseries_per_month[1]["y"], 7)
