from django.test import TestCase
from django.urls import reverse

from categories.factories import CategoryFactory
from core import constants
from questions.factories import QuestionFactory
from quizs.factories import QuizFactory
from quizs.models import QuizQuestion
from tags.factories import TagFactory
from users.factories import UserFactory


class QuizApiTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = UserFactory(first_name="First 1", last_name="Last 1")
        cls.user_2 = UserFactory(first_name="First 2", last_name="Last 2")
        cls.user_3 = UserFactory(first_name="First 3", last_name="Last 3")
        cls.category_1 = CategoryFactory(name="Cat 1")
        cls.tag_1 = TagFactory(name="Tag 1")
        cls.tag_2 = TagFactory(name="Tag 2")
        cls.tag_3 = TagFactory(name="Tag 3")
        cls.question_1 = QuestionFactory(
            text="question 1",
            category=cls.category_1,
            author=cls.user_1,
            validation_status=constants.VALIDATION_STATUS_IN_PROGRESS,
        )
        cls.question_2 = QuestionFactory(
            text="question 2",
            type=constants.QUESTION_TYPE_VF,
            difficulty=constants.QUESTION_DIFFICULTY_HARD,
            language=constants.LANGUAGE_ENGLISH,
            category=cls.category_1,
            answer_correct="a",
            # tags=[cls.tag_2, cls.tag_1],
            author=cls.user_2,
        )
        cls.question_2.tags.set([cls.tag_2, cls.tag_1])
        cls.question_3 = QuestionFactory(
            text="question 3",
            category=cls.category_1,
            # tags=[cls.tag_2],
            author=cls.user_3,
        )
        cls.question_3.tags.set([cls.tag_2])
        cls.quiz_1 = QuizFactory(name="quiz 1", publish=False)  # authors=[cls.user_1]
        cls.quiz_1.authors.set([cls.user_1])
        QuizQuestion.objects.create(quiz=cls.quiz_1, question=cls.question_1)
        cls.quiz_2 = QuizFactory(
            name="quiz 2",
            publish=False,
            language=constants.LANGUAGE_FRENCH,
            spotlight=True,
            # tags=[cls.tag_1],
            # authors=[cls.user_2],
        )
        cls.quiz_2.tags.set([cls.tag_1])
        cls.quiz_2.authors.set([cls.user_2])
        QuizQuestion.objects.create(quiz=cls.quiz_2, question=cls.question_2, order=2)
        QuizQuestion.objects.create(quiz=cls.quiz_2, question=cls.question_3, order=1)
        cls.quiz_2.publish = True  # cannot have a published quiz without any questions
        cls.quiz_2.save()
        cls.quiz_3 = QuizFactory(
            name="quiz 3",
            publish=False,
            language=constants.LANGUAGE_ENGLISH,
            spotlight=True,
            # tags=[cls.tag_2],
            # authors=[cls.user_2],
        )
        cls.quiz_3.tags.set([cls.tag_2])
        cls.quiz_3.authors.set([cls.user_2])
        QuizQuestion.objects.create(quiz=cls.quiz_3, question=cls.question_3, order=1)
        cls.quiz_3.publish = True  # cannot have a published quiz without any questions
        cls.quiz_3.save()

    def test_quiz_list(self):
        response = self.client.get(reverse("api:quiz-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data["results"], list)
        self.assertEqual(len(response.data["results"]), 2)  # 1 quiz not published
        self.assertIsNone(response.data["next"])  # pagination: 100
        # quiz questions
        self.assertEqual(response.data["results"][0]["id"], self.quiz_2.id)
        self.assertEqual(response.data["results"][0]["question_count"], 2)
        self.assertFalse("question" in response.data["results"][0])

    def test_quiz_list_filter_by_language(self):
        response = self.client.get(reverse("api:quiz-list"), {"language": constants.LANGUAGE_ENGLISH})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

    def test_quiz_list_filter_by_tag(self):
        response = self.client.get(reverse("api:quiz-list"), {"tags": self.tag_1.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        response = self.client.get(reverse("api:quiz-list"), {"tags": self.tag_3.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 0)

    def test_quiz_list_filter_by_author(self):
        response = self.client.get(reverse("api:quiz-list"), {"authors": self.user_1.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 0)  # quiz not published
        response = self.client.get(reverse("api:quiz-list"), {"authors": self.user_2.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)

    def test_quiz_list_filter_by_spotlight(self):
        response = self.client.get(reverse("api:quiz-list"), {"spotlight": True})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)

    def test_quiz_list_filter_limit(self):
        response = self.client.get(reverse("api:quiz-list"), {"limit": 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)  # paginates 1 result per page
        self.assertIsNotNone(response.data["next"])

    def test_quiz_list_order(self):
        response = self.client.get(reverse("api:quiz-list"), {"order": "id"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["id"], self.quiz_2.id)
        response = self.client.get(reverse("api:quiz-list"), {"order": "-id"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["id"], self.quiz_3.id)

    # def test_quiz_list_with_question_order(self):
    #     response = self.client.get(reverse("api:quiz-list"), {"question_order": "true"})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsInstance(response.data["results"], list)
    #     self.assertEqual(len(response.data["results"]), 1)  # 1 quiz not published
    #     self.assertEqual(len(response.data["results"][0]["questions"]), 2)
    #     self.assertEqual(response.data["results"][0]["questions"][0]["id"], self.question_3.id)
    #     self.assertEqual(response.data["results"][0]["questions"][0]["order"], 1)

    # def test_quiz_list_full(self):
    #     response = self.client.get(reverse("api:quiz-list"), {"full": "true"})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsInstance(response.data["results"], list)
    #     self.assertEqual(len(response.data["results"]), 1)  # 1 quiz not published
    #     self.assertEqual(len(response.data["results"][0]["questions"]), 2)
    #     self.assertEqual(response.data["results"][0]["questions"][0]["id"], self.question_2.id)

    def test_quiz_detail(self):
        response = self.client.get(reverse("api:quiz-detail", args=[self.quiz_2.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        # questions
        self.assertEqual(response.data["question_count"], 2)
        self.assertEqual(len(response.data["questions"]), 2)
