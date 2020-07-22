from django.test import TestCase

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


class QuestionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.question_1 = Question.objects.create(answer_correct="a")
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

    def test_question_agg_stat_created(self):
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(QuestionAggStat.objects.count(), 1)
        question_agg_stat = QuestionAggStat.objects.first()
        self.assertEqual(question_agg_stat.question_id, self.question_1.id)

    def test_answer_count(self):
        self.assertEqual(self.question_1.answer_count_agg, 6)
        self.assertEqual(self.question_1.answer_success_count_agg, 3)
        self.assertEqual(self.question_1.answer_success_rate, 50)

    def test_feedback_count(self):
        self.assertEqual(self.question_1.like_count_agg, 2)
        self.assertEqual(self.question_1.dislike_count_agg, 1)


class QuizModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.question_1 = Question.objects.create(answer_correct="a")
        cls.quiz_1 = Quiz.objects.create(like_count=2)
        cls.quiz_1.questions.set([cls.question_1.id])
        QuestionAnswerEvent.objects.create(
            question_id=cls.question_1.id, choice="a", source="question"
        )
        QuizAnswerEvent.objects.create(quiz_id=cls.quiz_1.id, answer_success_count=1)
        QuizFeedbackEvent.objects.create(quiz_id=cls.quiz_1.id, choice="dislike")

    def test_answer_count(self):
        self.assertEqual(self.quiz_1.answer_count_agg, 1)

    def test_feedback_count(self):
        self.assertEqual(self.quiz_1.like_count, 2)
        self.assertEqual(self.quiz_1.dislike_count, 0)
        self.assertEqual(self.quiz_1.like_count_agg, 2)
        self.assertEqual(self.quiz_1.dislike_count_agg, 1)


class DailyStatModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.question_1 = Question.objects.create(answer_correct="a")
        QuestionAnswerEvent.objects.create(
            question_id=cls.question_1.id, choice="a", source="question"
        )
        DailyStat.objects.create(
            date="2020-04-30", question_answer_count=10, question_feedback_count=5
        )
        DailyStat.objects.create(
            date="2020-04-29", question_answer_count=2, question_feedback_count=1
        )

    def test_question_answer_count_count(self):
        self.assertEqual(DailyStat.objects.overall_question_answer_count(), 12)
        self.assertEqual(DailyStat.objects.overall_question_feedback_count(), 6)
        self.assertEqual(DailyStat.objects.overall_quiz_answer_count(), 0)
