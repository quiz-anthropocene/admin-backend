from django.test import TestCase
from django.core.exceptions import ValidationError

from api import constants
from api.models import (
    Question,
    QuestionAggStat,
    QuestionAnswerEvent,
    QuestionFeedbackEvent,
    QuizAnswerEvent,
    QuizFeedbackEvent,
    DailyStat,
)
from api.tests.factories import QuestionFactory, QuizFactory


class QuestionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.question_1 = QuestionFactory(answer_correct="a")
        cls.question_1.agg_stats.answer_count = 5
        cls.question_1.agg_stats.answer_success_count = 2
        cls.question_1.agg_stats.like_count = 2
        cls.question_1.agg_stats.save()
        QuestionAnswerEvent.objects.create(
            question_id=cls.question_1.id, choice="a", source="question"
        )
        QuestionFeedbackEvent.objects.create(
            question_id=cls.question_1.id, choice="dislike", source="quiz"
        )
        cls.question_rm_1 = QuestionFactory(
            type=constants.QUESTION_TYPE_QCM_RM, answer_correct="ab"
        )
        cls.question_rm_2 = QuestionFactory(
            type=constants.QUESTION_TYPE_QCM_RM, answer_correct="abc"
        )
        cls.question_rm_3 = QuestionFactory(
            type=constants.QUESTION_TYPE_QCM_RM, answer_correct="abcd"
        )
        QuestionAnswerEvent.objects.create(
            question_id=cls.question_rm_1.id, choice="cd", source="question"
        )
        cls.question_vf = QuestionFactory(
            type=constants.QUESTION_TYPE_VF, answer_correct="b"
        )

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

    def test_validated_question_must_have_category(self):
        self.assertRaises(ValidationError, QuestionFactory, category=None)

    def test_validated_question_must_have_correct_choice_fields(self):
        self.assertRaises(ValidationError, QuestionFactory, type="Coucou")
        self.assertRaises(ValidationError, QuestionFactory, difficulty=42)
        self.assertRaises(
            ValidationError, QuestionFactory, answer_correct="La réponse D"
        )
        self.assertRaises(ValidationError, QuestionFactory, validation_status="TBD")

    def test_validated_question_qcm_must_have_one_answer(self):
        self.assertRaises(ValidationError, QuestionFactory, answer_correct="")
        self.assertRaises(ValidationError, QuestionFactory, answer_correct="ab")
        self.assertRaises(ValidationError, QuestionFactory, answer_correct="aa")

    def test_validated_question_qcm_rm_must_have_at_least_two_answers(self):
        self.assertRaises(
            ValidationError,
            QuestionFactory,
            type=constants.QUESTION_TYPE_QCM_RM,
            answer_correct="",
        )
        self.assertRaises(
            ValidationError,
            QuestionFactory,
            type=constants.QUESTION_TYPE_QCM_RM,
            answer_correct="a",
        )
        self.assertRaises(
            ValidationError,
            QuestionFactory,
            type=constants.QUESTION_TYPE_QCM_RM,
            answer_correct="ba",
        )
        self.assertRaises(
            ValidationError,
            QuestionFactory,
            type=constants.QUESTION_TYPE_QCM_RM,
            answer_correct="aab",
        )
        self.assertRaises(
            ValidationError,
            QuestionFactory,
            type=constants.QUESTION_TYPE_QCM_RM,
            answer_correct="abcde",
        )

    def test_validated_question_vf_must_have_specific_answer(self):
        self.assertRaises(
            ValidationError,
            QuestionFactory,
            type=constants.QUESTION_TYPE_VF,
            answer_correct="",
        )
        self.assertRaises(
            ValidationError,
            QuestionFactory,
            type=constants.QUESTION_TYPE_VF,
            answer_correct="c",
        )
        self.assertRaises(
            ValidationError,
            QuestionFactory,
            type=constants.QUESTION_TYPE_VF,
            answer_correct="ab",
        )

    def test_validated_question_vf_must_have_ordered_answers(self):
        self.assertRaises(
            ValidationError,
            QuestionFactory,
            type=constants.QUESTION_TYPE_VF,
            has_ordered_answers=False,
        )

    # def test_validated_question_must_have_publish(self):
    #     self.assertRaises(
    #         ValidationError, QuestionFactory, publish=False,
    #     )


class QuizModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.question_1 = QuestionFactory(answer_correct="a")
        cls.quiz_1 = QuizFactory(name="quiz 1")
        cls.quiz_1.questions.set([cls.question_1.id])
        QuestionAnswerEvent.objects.create(
            question_id=cls.question_1.id, choice="a", source="question"
        )
        QuizAnswerEvent.objects.create(quiz_id=cls.quiz_1.id, answer_success_count=1)
        QuizFeedbackEvent.objects.create(quiz_id=cls.quiz_1.id, choice="dislike")

    def test_answer_count(self):
        self.assertEqual(self.quiz_1.answer_count_agg, 1)

    def test_feedback_count(self):
        self.assertEqual(self.quiz_1.like_count_agg, 0)
        self.assertEqual(self.quiz_1.dislike_count_agg, 1)

    def test_published_quiz_must_have_at_least_one_question(self):
        self.quiz_not_published = QuizFactory(name="quiz not published")
        self.quiz_not_published.publish = True
        self.assertRaises(
            ValidationError, self.quiz_not_published.save, update_fields=["publish"]
        )

    def test_published_quiz_must_have_published_questions(self):
        self.question_published = QuestionFactory(answer_correct="a")
        self.question_not_published = QuestionFactory(
            answer_correct="a",
            validation_status=constants.QUESTION_VALIDATION_STATUS_IN_PROGRESS,
            publish=False,
        )
        self.quiz_published = QuizFactory(name="quiz published", publish=True)
        self.quiz_not_published = QuizFactory(name="quiz not published")
        # pass
        self.quiz_not_published.questions.set(
            [self.question_published, self.question_not_published]
        )
        # fail
        self.assertRaises(
            ValidationError,
            self.quiz_published.questions.set,
            [self.question_published, self.question_not_published],
        )


class DailyStatModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.question_1 = QuestionFactory(answer_correct="a")
        QuestionAnswerEvent.objects.create(
            question_id=cls.question_1.id, choice="a", source="question"
        )
        # 3 daily stats in the same week
        DailyStat.objects.create(
            date="2020-04-30", question_answer_count=10, question_feedback_count=5
        )
        DailyStat.objects.create(
            date="2020-05-01", question_answer_count=2, question_feedback_count=1
        )
        DailyStat.objects.create(
            date="2020-05-02", question_answer_count=4, question_feedback_count=2
        )
        # 1 daily stats in the next week
        DailyStat.objects.create(
            date="2020-05-06", question_answer_count=1, question_feedback_count=1
        )

    def test_question_answer_count_count(self):
        self.assertEqual(DailyStat.objects.agg_count("question_answer_count"), 17)
        self.assertEqual(DailyStat.objects.agg_count("question_feedback_count"), 9)
        self.assertEqual(DailyStat.objects.agg_count("quiz_answer_count"), 0)
        self.assertEqual(
            DailyStat.objects.agg_count(
                "question_answer_count", since="week", week_or_month_iso_number=18
            ),
            16,
        )
        self.assertEqual(
            DailyStat.objects.agg_count(
                "question_answer_count", since="month", week_or_month_iso_number=4
            ),
            10,
        )
        self.assertEqual(
            DailyStat.objects.agg_count(
                "question_feedback_count", since="month", week_or_month_iso_number=5
            ),
            4,
        )
        agg_timeseries_per_day_1 = DailyStat.objects.agg_timeseries(
            field="question_answer_count", scale="day"
        )
        self.assertEqual(len(agg_timeseries_per_day_1), 4)
        self.assertEqual(agg_timeseries_per_day_1[0]["day"], "2020-04-30")
        agg_timeseries_per_day_2 = DailyStat.objects.agg_timeseries(
            field="question_answer_count", scale="day", since_date="2020-05-02"
        )
        self.assertEqual(len(agg_timeseries_per_day_2), 2)
        self.assertEqual(agg_timeseries_per_day_2[0]["day"], "2020-05-02")
        agg_timeseries_per_month = DailyStat.objects.agg_timeseries(
            field="question_answer_count", scale="month"
        )
        self.assertEqual(len(agg_timeseries_per_month), 2)
        self.assertEqual(agg_timeseries_per_month[0]["day"], "2020-04-01")
        self.assertEqual(agg_timeseries_per_month[0]["y"], 10)
        self.assertEqual(agg_timeseries_per_month[1]["day"], "2020-05-01")
        self.assertEqual(agg_timeseries_per_month[1]["y"], 7)
