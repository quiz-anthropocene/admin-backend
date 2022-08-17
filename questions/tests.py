from django.test import TestCase

from categories.factories import CategoryFactory
from core import constants
from questions.factories import QuestionFactory
from questions.models import Question
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


class QuestionModelHistoryTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category_1 = CategoryFactory(name="Cat 1")
        cls.category_2 = CategoryFactory(name="Cat 2")
        cls.tag_1 = TagFactory(name="Tag 1")
        cls.tag_2 = TagFactory(name="Another tag")
        cls.tag_3 = TagFactory(name="Tag 3")
        cls.question = QuestionFactory(
            text="Test", category=cls.category_1, validation_status=constants.VALIDATION_STATUS_NEW
        )
        cls.question.tags.set([cls.tag_1, cls.tag_2])

    def test_history_object_on_create(self):
        self.assertEqual(self.question.history.count(), 1 + 1)
        create_history_item = self.question.history.last()
        self.assertEqual(create_history_item.history_type, "+")
        self.assertEqual(create_history_item.text, self.question.text)
        CHANGE_FIELDS = [
            "text",
            "type",
            "difficulty",
            "language",
            "answer_option_a",
            "answer_option_b",
            "answer_correct",
            "has_ordered_answers",
            "validation_status",
            "visibility",
        ]  # "category"
        for field in CHANGE_FIELDS:
            self.assertTrue(field in create_history_item.history_changed_fields)
        self.assertEqual(len(create_history_item.tag_list), 0)
        update_history_item = self.question.history.first()
        self.assertEqual(update_history_item.history_type, "~")
        self.assertEqual(update_history_item.text, self.question.text)
        self.assertEqual(len(update_history_item.tag_list), 2)
        self.assertEqual(update_history_item.history_changed_fields, ["tag_list"])

    def test_history_object_created_on_save(self):
        self.question.answer_option_a = "réponse A"
        self.question.answer_option_b = "réponse B"
        self.question.category = self.category_2
        self.question.save()
        self.assertEqual(self.question.history.count(), 2 + 1)
        update_history_item = self.question.history.first()
        self.assertEqual(update_history_item.history_type, "~")
        self.assertEqual(update_history_item.category_string, self.category_2.name)
        self.assertEqual(
            update_history_item.history_changed_fields, ["answer_option_a", "answer_option_b", "category"]
        )

    def test_history_diff(self):
        self.question.text = "La vraie question"
        self.question.validation_status = constants.VALIDATION_STATUS_OK
        self.question.category = self.category_2
        self.question.save()
        self.assertEqual(self.question.history.count(), 2 + 1)
        update_history_item = self.question.history.first()
        previous_history_item = self.question.history.first().prev_record
        delta = update_history_item.diff_against(previous_history_item)
        self.assertEqual(len(delta.changes), 4)
        CHANGE_FIELDS = ["text", "validation_status", "category", "category_string"]
        delta_change_fields = [change.field for change in delta.changes]
        for field in CHANGE_FIELDS:
            self.assertTrue(field in delta_change_fields)
        for field in ["text", "validation_status", "category"]:  # "category_string" ignored
            self.assertTrue(field in update_history_item.history_changed_fields)


class QuestionModelQuerySetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_contributor = UserFactory()
        QuestionFactory(validation_status=constants.VALIDATION_STATUS_OK, visibility=constants.VISIBILITY_PUBLIC)
        QuestionFactory(validation_status=constants.VALIDATION_STATUS_OK, visibility=constants.VISIBILITY_HIDDEN)
        QuestionFactory(validation_status=constants.VALIDATION_STATUS_OK, visibility=constants.VISIBILITY_PRIVATE)
        QuestionFactory(validation_status=constants.VALIDATION_STATUS_NEW, visibility=constants.VISIBILITY_PUBLIC)
        QuestionFactory(validation_status=constants.VALIDATION_STATUS_NEW, visibility=constants.VISIBILITY_HIDDEN)
        QuestionFactory(
            text="xyz",
            validation_status=constants.VALIDATION_STATUS_NEW,
            visibility=constants.VISIBILITY_PRIVATE,
            author=cls.user_contributor,
        )

    def test_question_validated(self):
        self.assertEqual(Question.objects.validated().count(), 3)

    def test_question_not_validated(self):
        self.assertEqual(Question.objects.not_validated().count(), 3)

    def test_question_public(self):
        self.assertEqual(Question.objects.public().count(), 4)

    def test_question_public_validated(self):
        self.assertEqual(Question.objects.public().validated().count(), 2)

    def test_public_or_by_author(self):
        self.assertEqual(Question.objects.public_or_by_author().count(), 4)  # public
        self.assertEqual(
            Question.objects.public_or_by_author(author=self.user_contributor).count(), 4 + 1
        )  # public + author

    def test_simple_search(self):
        self.assertEqual(Question.objects.simple_search(value="xy").count(), 1)
