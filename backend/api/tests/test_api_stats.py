from django.test import TestCase
from django.urls import reverse

from api.tests.factories import QuestionFactory, QuizFactory


class ApiStatTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.question_1 = QuestionFactory(text="question 1")
        cls.question_2 = QuestionFactory(text="question 2")
        cls.quiz_1 = QuizFactory(name="quiz 1")
        cls.quiz_2 = QuizFactory(name="quiz 2")

    def test_question_answer_event(self):
        response = self.client.post(
            reverse("stats:question-answer-event-list"),
            data={"question": self.question_2.id, "choice": "a", "source": "question"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["choice"], "a")
        self.assertEqual(self.question_2.stats.count(), 1)
        self.assertEqual(self.question_2.answer_count_agg, 1)
        self.assertEqual(self.question_2.answer_success_count_agg, 1)
        self.assertEqual(self.question_2.answer_success_rate, 100)

        response = self.client.post(
            reverse("stats:question-answer-event-list"),
            data={"question": self.question_2.id, "choice": "b", "source": "quiz"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["choice"], "b")
        self.assertEqual(self.question_2.stats.count(), 1 + 1)
        self.assertEqual(self.question_2.answer_count_agg, 1 + 1)
        self.assertEqual(self.question_2.answer_success_count_agg, 1)
        self.assertEqual(self.question_2.answer_success_rate, 50)

        # won't work if the question_id is missing or wrong
        response = self.client.post(
            reverse("stats:question-answer-event-list"),
            data={"choice": "b", "source": "quiz"},
        )
        self.assertNotEqual(response.status_code, 201)
        response = self.client.post(
            reverse("stats:question-answer-event-list"),
            data={"question": self.question_2.id + 1, "choice": "b", "source": "quiz"},
        )
        self.assertNotEqual(response.status_code, 201)

    def test_question_feedback_event(self):
        response = self.client.post(
            reverse("stats:question-feedback-event-list"),
            data={"question": self.question_2.id, "choice": "like", "source": "question"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["choice"], "like")
        self.assertEqual(self.question_2.feedbacks.count(), 1)
        self.assertEqual(self.question_2.like_count_agg, 1)
        self.assertEqual(self.question_2.dislike_count_agg, 0)

        response = self.client.post(
            reverse("stats:question-feedback-event-list"),
            data={"question": self.question_2.id, "choice": "dislike", "source": "question"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["choice"], "dislike")
        self.assertEqual(self.question_2.feedbacks.count(), 2)
        self.assertEqual(self.question_2.like_count_agg, 1)
        self.assertEqual(self.question_2.dislike_count_agg, 1)

    def test_quiz_answer_event(self):
        response = self.client.post(
            reverse("stats:quiz-answer-event-list"),
            data={"quiz": self.quiz_2.id, "answer_success_count": 1, "duration_seconds": 40},
        )
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["answer_success_count"], 1)
        self.assertEqual(self.quiz_2.stats.count(), 1)
        self.assertEqual(self.quiz_2.answer_count_agg, 1)
        self.assertEqual(self.quiz_2.duration_average_seconds, 40)
        self.assertEqual(self.quiz_2.duration_average_minutes_string, "0min40")

        response = self.client.post(
            reverse("stats:quiz-answer-event-list"),
            data={"quiz": self.quiz_2.id, "answer_success_count": 2, "duration_seconds": 80},
        )
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["answer_success_count"], 2)
        self.assertEqual(self.quiz_2.stats.count(), 2)
        self.assertEqual(self.quiz_2.duration_average_seconds, 60)
        self.assertEqual(self.quiz_2.duration_average_minutes_string, "1min00")


    def test_quiz_feedback_event(self):
        response = self.client.post(
            reverse("stats:quiz-feedback-event-list"),
            data={"quiz": self.quiz_2.id, "choice": "like"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["choice"], "like")
        self.assertEqual(self.quiz_2.feedbacks.count(), 1)
        self.assertEqual(self.quiz_2.like_count_agg, 1)
        self.assertEqual(self.quiz_2.dislike_count_agg, 0)

        response = self.client.post(
            reverse("stats:quiz-feedback-event-list"),
            data={"quiz": self.quiz_2.id, "choice": "dislike"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["choice"], "dislike")
        self.assertEqual(self.quiz_2.feedbacks.count(), 2)
        self.assertEqual(self.quiz_2.like_count_agg, 1)
        self.assertEqual(self.quiz_2.dislike_count_agg, 1)
