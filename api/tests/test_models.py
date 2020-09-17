from django.test import TestCase
from django.core.exceptions import ValidationError

from api import constants
from api.models import (
    Question,
    QuestionAggStat,
    QuestionAnswerEvent,
    QuestionFeedbackEvent,
    Quiz,
    QuizAnswerEvent,
    QuizFeedbackEvent,
    DailyStat,
)
from api.tests.factories import QuestionFactory


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

    def test_question_must_have_correct_choice_fields(self):
        self.assertRaises(ValidationError, QuestionFactory, type="Coucou")
        self.assertRaises(ValidationError, QuestionFactory, difficulty=42)
        self.assertRaises(
            ValidationError, QuestionFactory, answer_correct="La réponse D"
        )
        self.assertRaises(ValidationError, QuestionFactory, validation_status="TBD")

    def test_question_qcm_must_have_one_answer(self):
        self.assertRaises(ValidationError, QuestionFactory, answer_correct="")
        self.assertRaises(ValidationError, QuestionFactory, answer_correct="ab")
        self.assertRaises(ValidationError, QuestionFactory, answer_correct="aa")

    def test_question_qcm_rm_must_have_at_least_two_answers(self):
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

    def test_question_vf_must_have_specific_answer(self):
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


class QuizModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.question_1 = QuestionFactory(answer_correct="a")
        cls.quiz_1 = Quiz.objects.create(name="quiz 1")
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


class DailyStatModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.question_1 = QuestionFactory(answer_correct="a")
        QuestionAnswerEvent.objects.create(
            question_id=cls.question_1.id, choice="a", source="question"
        )
        DailyStat.objects.create(
            date="2020-04-30", question_answer_count=10, question_feedback_count=5
        )
        DailyStat.objects.create(
            date="2020-05-01", question_answer_count=2, question_feedback_count=1
        )

    def test_question_answer_count_count(self):
        self.assertEqual(DailyStat.objects.agg_count("question_answer_count"), 12)
        self.assertEqual(DailyStat.objects.agg_count("question_feedback_count"), 6)
        self.assertEqual(DailyStat.objects.agg_count("quiz_answer_count"), 0)
        self.assertEqual(
            DailyStat.objects.agg_count(
                "question_answer_count", since="week", week_or_month_iso_number=18
            ),
            12,
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
            1,
        )
