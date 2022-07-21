from django.test import TestCase
from django.urls import reverse

from categories.factories import CategoryFactory
from core import constants
from questions.factories import QuestionFactory
from quizs.factories import QuizFactory
from quizs.models import QuizQuestion
from tags.factories import TagFactory
from users.factories import UserFactory


class ApiTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = UserFactory(first_name="First 1", last_name="Last 1")
        cls.user_2 = UserFactory(first_name="First 2", last_name="Last 2")
        cls.user_3 = UserFactory(first_name="First 3", last_name="Last 3")
        cls.category_1 = CategoryFactory(name="Cat 1")
        cls.tag_1 = TagFactory(name="Tag 1")
        cls.tag_2 = TagFactory(name="Tag 2")
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
            author=cls.user_2,
        )
        cls.question_2.tags.set([cls.tag_2, cls.tag_1])
        cls.question_3 = QuestionFactory(text="question 3", category=cls.category_1, author=cls.user_3)
        cls.question_3.tags.add(cls.tag_2)
        cls.question_3.save()
        cls.quiz_1 = QuizFactory(name="quiz 1", publish=False, author=cls.user_1)
        QuizQuestion.objects.create(quiz=cls.quiz_1, question=cls.question_1)
        cls.quiz_2 = QuizFactory(
            name="quiz 2",
            publish=False,
            language=constants.LANGUAGE_ENGLISH,
            author=cls.user_2,
        )
        cls.quiz_2.tags.set([cls.tag_1])
        QuizQuestion.objects.create(quiz=cls.quiz_2, question=cls.question_2, order=2)
        QuizQuestion.objects.create(quiz=cls.quiz_2, question=cls.question_3, order=1)
        cls.quiz_2.publish = True  # cannot have a published quiz without any questions
        cls.quiz_2.save()

    def test_root(self):
        response = self.client.get(reverse("api:index"))
        self.assertEqual(response.status_code, 200)
        html = response.content.decode("utf8")
        self.assertIn("API", html)

    def test_question_list(self):
        response = self.client.get(reverse("api:question-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)
        self.assertIsInstance(response.data["results"], list)
        self.assertEqual(len(response.data["results"]), 2)  # 1 question not validated

    def test_question_list_filter_by_type(self):
        response = self.client.get(reverse("api:question-list"), {"type": constants.QUESTION_TYPE_VF})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

    def test_question_list_filter_by_difficulty(self):
        response = self.client.get(
            reverse("api:question-list"),
            {"difficulty": constants.QUESTION_DIFFICULTY_HARD},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

    def test_question_list_filter_by_language(self):
        response = self.client.get(reverse("api:question-list"), {"language": constants.LANGUAGE_ENGLISH})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

    def test_question_list_filter_by_category(self):
        response = self.client.get(reverse("api:question-list"), {"category": self.category_1.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)  # 1 question not validated

    def test_question_list_filter_by_tag(self):
        response = self.client.get(reverse("api:question-list"), {"tags": self.tag_1.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

        response = self.client.get(reverse("api:question-list"), {"tags": self.tag_2.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)

    def test_question_list_filter_by_author(self):
        response = self.client.get(reverse("api:question-list"), {"author": self.user_1.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 0)  # question not validated
        response = self.client.get(reverse("api:question-list"), {"author": self.user_2.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

    def test_question_detail(self):
        response = self.client.get(reverse("api:question-detail", args=[self.question_2.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertIsInstance(response.data["category"], int)
        self.assertEqual(response.data["category"], self.category_1.id)
        self.assertEqual(len(response.data["tags"]), 2)
        self.assertIsInstance(response.data["tags"][0], int)
        self.assertEqual(response.data["tags"][0], self.tag_1.id)

    # def test_question_detail_full_string(self):
    #     response = self.client.get(
    #         reverse("api:question-detail", args=[self.question_2.id]) + "?full=true"
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsInstance(response.data, dict)
    #     self.assertIsInstance(response.data["category"], str)
    #     self.assertEqual(response.data["category"], self.category_1.name)
    #     self.assertEqual(len(response.data["tags"]), 2)
    #     self.assertIsInstance(response.data["tags"][0], str)
    #     self.assertEqual(response.data["tags"][0], self.tag_1.name)

    # def test_question_detail_full_object(self):
    #     response = self.client.get(
    #         reverse("api:question_detail", args=[self.question_2.id]) + "?full=object"
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsInstance(response.data, dict)
    #     self.assertIsInstance(response.data["category"]["name"], dict)
    #     self.assertEqual(response.data["category"], self.category_1.name)
    #     self.assertEqual(len(response.data["tags"]), 2)
    #     self.assertIsInstance(response.data["tags"][0]["name"], dict)
    #     self.assertEqual(response.data["tags"][0], self.tag_1.name)

    # def test_question_stats(self):
    #     response = self.client.get(
    #         reverse("stats:question_stats", args=[self.question_2.id])
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsInstance(response.data, dict)
    #     self.assertEqual(response.data["question_id"], self.question_2.id)

    # def test_question_random(self):
    #     response = self.client.get(reverse("api:question_random"))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsInstance(response.data, dict)
    #     self.assertIn(response.data["id"], [self.question_2.id, self.question_3.id])

    def test_question_type_list(self):
        response = self.client.get(reverse("api:question-type-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data["results"], list)
        self.assertEqual(len(response.data["results"]), 3)

    def test_question_difficulty_list(self):
        response = self.client.get(reverse("api:question-difficulty-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data["results"], list)
        self.assertEqual(len(response.data["results"]), 5)

    def test_question_language_list(self):
        response = self.client.get(reverse("api:question-language-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data["results"], list)
        self.assertEqual(len(response.data["results"]), 3)

    def test_question_validation_status_list(self):
        response = self.client.get(reverse("api:question-validation-status-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data["results"], list)
        self.assertEqual(len(response.data["results"]), 5)

    def test_category_list(self):
        response = self.client.get(reverse("api:category-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data["results"], list)
        self.assertEqual(len(response.data["results"]), 1)

    def test_tag_list(self):
        response = self.client.get(reverse("api:tag-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data["results"], list)
        self.assertEqual(len(response.data["results"]), 2)

    # def test_author_list(self):
    #     response = self.client.get(reverse("api:author_list"))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsInstance(response.data["results"], list)
    #     self.assertEqual(len(response.data["results"]), 2)  # 1 question not validated

    def test_quiz_list(self):
        response = self.client.get(reverse("api:quiz-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data["results"], list)
        self.assertEqual(len(response.data["results"]), 1)  # 1 quiz not published
        # self.assertEqual(response.data["results"][0]["question_count"], 2)
        # self.assertEqual(response.data["results"][0]["questions"][0], self.question_2.id)

    def test_quiz_list_filter_by_language(self):
        response = self.client.get(reverse("api:quiz-list"), {"language": constants.LANGUAGE_ENGLISH})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

    def test_quiz_list_filter_by_tag(self):
        response = self.client.get(reverse("api:quiz-list"), {"tags": self.tag_1.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

        response = self.client.get(reverse("api:quiz-list"), {"tags": self.tag_2.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 0)

    def test_quiz_list_filter_by_author(self):
        response = self.client.get(reverse("api:quiz-list"), {"author": self.user_1.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 0)  # quiz not published
        response = self.client.get(reverse("api:quiz-list"), {"author": self.user_2.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

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
