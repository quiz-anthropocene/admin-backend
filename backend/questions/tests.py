from django.test import TestCase

from categories.factories import CategoryFactory
from questions.factories import QuestionFactory
from quizs.factories import QuizFactory
from quizs.models import QuizQuestion
from tags.factories import TagFactory
from users.factories import UserFactory


class QuestionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.question = QuestionFactory()
        cls.tag_1 = TagFactory(name="Tag 1")
        cls.tag_2 = TagFactory(name="Another tag")
        cls.question.tags.set([cls.tag_1, cls.tag_2])
        cls.quiz = QuizFactory(name="Le premier quiz")
        cls.quiz.questions.add(cls.question)

    def test_str(self):
        self.assertTrue(str(self.question.id) in str(self.question))
        self.assertTrue(self.question.text in str(self.question))
        self.assertTrue(self.question.category.name not in str(self.question))

    def test_tags_list(self):
        self.assertEqual(len(self.question.tags_list), 2)
        self.assertEqual(self.question.tags_list[0], self.tag_2.name)

    def test_quizs_list(self):
        self.assertEqual(len(self.question.quizs_list), 1)
        self.assertEqual(self.question.quizs_list[0], self.quiz.name)

    def test_quiz_count(self):
        self.assertEqual(self.question.quiz_count, 1)


class QuestionModelSaveTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.question = QuestionFactory()
        cls.tag_1 = TagFactory(name="Tag 1")
        cls.tag_2 = TagFactory(name="Another tag")
        cls.question.tags.set([cls.tag_1, cls.tag_2])

    def test_update_related_flatten_fields_on_save(self):
        category = CategoryFactory(name="Climat")
        self.question.category = category
        user_1 = UserFactory(first_name="Paul", last_name="Dupont")
        user_2 = UserFactory(first_name="Marie", last_name="Dupond")
        self.question.author = user_1
        self.question.validator = user_2
        self.question.save()
        self.assertEqual(self.question.category_string, category.name)
        self.assertEqual(self.question.author_string, user_1.full_name)
        self.assertEqual(self.question.validator_string, user_2.full_name)

    def test_update_m2m_flatten_fields_on_save(self):
        tag_3 = TagFactory(name="ABC")
        self.question.tags.add(tag_3)
        # self.question.save()  # no need to run save(), m2m_changed signal was triggered above
        self.assertEqual(self.question.tags.count(), 2 + 1)
        self.assertEqual(len(self.question.tag_list), 3)
        self.assertEqual(self.question.tag_list[0], tag_3.name)

    def test_update_m2m_through_flatten_fields_on_save(self):
        quiz_1 = QuizFactory(name="Quiz 1")
        QuizQuestion.objects.create(question=self.question, quiz=quiz_1, order=5)
        # self.question.save()  # no need to run save(), m2m_changed signal was triggered above
        self.assertEqual(self.question.quizs.count(), 1)
        self.assertEqual(len(self.question.quizs_id_list), 1)
        self.assertEqual(self.question.quizs_id_list[0], quiz_1.id)
        quiz_2 = QuizFactory(name="Un autre quiz")
        self.question.quizs.add(quiz_2, through_defaults={"order": 3})
        # self.question.save()  # no need to run save(), m2m_changed signal was triggered above
        self.assertEqual(self.question.quizs.count(), 2)
        self.assertEqual(len(self.question.quizs_id_list), 2)
        self.assertEqual(self.question.quizs_id_list[1], quiz_2.id)
