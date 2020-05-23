from django.test import TestCase

from api.models import Question, QuestionStat, QuestionFeedback


class QuestionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.question_1 = Question.objects.create(
            answer_correct="a", answer_count=5, answer_success_count=2, like_count=2
        )
        QuestionStat.objects.create(
            question_id=cls.question_1.id, choice="a", source="question"
        )
        QuestionFeedback.objects.create(
            question_id=cls.question_1.id, choice="dislike", source="quiz"
        )

    def test_answer_count(self):
        self.assertEqual(self.question_1.answer_count, 5)
        self.assertEqual(self.question_1.answer_success_count, 2)
        self.assertEqual(self.question_1.answer_count_agg, 6)
        self.assertEqual(self.question_1.answer_success_count_agg, 3)
        self.assertEqual(self.question_1.answer_success_rate, 50)

    def test_feedback_count(self):
        self.assertEqual(self.question_1.like_count, 2)
        self.assertEqual(self.question_1.dislike_count, 0)
        self.assertEqual(self.question_1.like_count_agg, 2)
        self.assertEqual(self.question_1.dislike_count_agg, 1)
