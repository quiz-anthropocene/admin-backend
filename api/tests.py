from django.test import TestCase
from django.urls import reverse

from api import models


class ApiTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category_1 = models.Category.objects.create(name="Cat 1")
        cls.tag_1 = models.Tag.objects.create(name="Tag 1")
        cls.tag_2 = models.Tag.objects.create(name="Tag 2")
        cls.question_1 = models.Question.objects.create(
            publish=False, author="author 1"
        )
        cls.question_2 = models.Question.objects.create(
            publish=True, author="author 2", category=cls.category_1, answer_correct="a"
        )
        cls.question_2.tags.set([cls.tag_2, cls.tag_1])
        cls.question_3 = models.Question.objects.create(publish=True, author="author 3")
        cls.question_3.tags.add(cls.tag_2)
        cls.question_3.save()
        cls.quiz_1 = models.Quiz.objects.create(name="quiz 1", publish=False)
        cls.quiz_1.questions.set([cls.question_1.id])
        cls.quiz_2 = models.Quiz.objects.create(name="quiz 2", publish=True)
        cls.quiz_2.questions.set([cls.question_2.id, cls.question_3.id])

    def test_root(self):
        response = self.client.get(reverse("api:index"))
        self.assertEqual(response.status_code, 200)
        html = response.content.decode("utf8")
        self.assertIn("Welcome", html)

    def test_question_list(self):
        response = self.client.get(reverse("api:question_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 2)  # 1 question not published

        response = self.client.get(reverse("api:question_list"), {"author": "author 1"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
        response = self.client.get(reverse("api:question_list"), {"author": "author 2"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        response = self.client.get(
            reverse("api:question_list"), {"tag": self.tag_1.name}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        response = self.client.get(
            reverse("api:question_list"), {"tag": self.tag_2.name}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        response = self.client.get(
            reverse("api:question_list"), {"category": self.category_1.name}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_question_detail(self):
        response = self.client.get(
            reverse("api:question_detail", args=[self.question_2.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["category"], self.category_1.name)
        self.assertEqual(len(response.data["tags"]), 2)
        self.assertEqual(response.data["tags"][0], self.tag_1.name)

    def test_question_random(self):
        response = self.client.get(reverse("api:question_random"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertIn(response.data["id"], [self.question_2.id, self.question_3.id])

    def test_question_count(self):
        response = self.client.get(reverse("api:question_count"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, int)
        self.assertEqual(response.data, 2)  # 1 question not published

    def test_category_list(self):
        response = self.client.get(reverse("api:category_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)

    def test_tag_list(self):
        response = self.client.get(reverse("api:tag_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 2)

    def test_author_list(self):
        response = self.client.get(reverse("api:author_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 2)  # 1 question not published

    def test_difficulty_level_list(self):
        response = self.client.get(reverse("api:difficulty_level_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 5)

    def test_quiz_list(self):
        response = self.client.get(reverse("api:quiz_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)  # 1 quiz not published
        self.assertEqual(response.data[0]["question_count"], 2)

    def test_quiz_list_full(self):
        response = self.client.get(reverse("api:quiz_list"), {"full": "true"})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)  # 1 quiz not published
        self.assertEqual(len(response.data[0]["questions"]), 2)

    def test_question_feedback(self):
        response = self.client.post(
            reverse("api:question_detail_feedbacks", args=[self.question_2.id]),
            data={
                "question": self.question_2.id,
                "choice": "like",
                "source": "question",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["choice"], "like")
        self.assertEqual(self.question_2.feedbacks.count(), 1)
        self.assertEqual(self.question_2.like_count_agg, 1)
        self.assertEqual(self.question_2.dislike_count_agg, 0)

        response = self.client.post(
            reverse("api:question_detail_feedbacks", args=[self.question_2.id]),
            data={
                "question": self.question_2.id,
                "choice": "dislike",
                "source": "question",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["choice"], "dislike")
        self.assertEqual(self.question_2.feedbacks.count(), 2)
        self.assertEqual(self.question_2.like_count_agg, 1)
        self.assertEqual(self.question_2.dislike_count_agg, 1)

    def test_question_stats(self):
        response = self.client.post(
            reverse("api:question_detail_stats", args=[self.question_2.id]),
            data={"question": self.question_2.id, "choice": "a", "source": "question"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["choice"], "a")
        self.assertEqual(self.question_2.stats.count(), 1)
        self.assertEqual(self.question_2.answer_count, 1)
        self.assertEqual(self.question_2.answer_success_count, 1)
        self.assertEqual(self.question_2.answer_success_rate, 100)

        response = self.client.post(
            reverse("api:question_detail_stats", args=[self.question_2.id]),
            data={"question": self.question_2.id, "choice": "b", "source": "question"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["choice"], "b")
        self.assertEqual(self.question_2.stats.count(), 2)
        self.assertEqual(self.question_2.answer_count, 2)
        self.assertEqual(self.question_2.answer_success_count, 1)
        self.assertEqual(self.question_2.answer_success_rate, 50)
