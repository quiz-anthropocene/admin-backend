from django.core.exceptions import ValidationError
from django.test import TestCase

from core import constants
from questions.factories import QuestionFactory
from quizs.factories import QuizFactory
from quizs.models import Quiz, QuizAuthor, QuizQuestion, QuizRelationship
from tags.factories import TagFactory
from users.factories import UserFactory


class QuizModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tag_1 = TagFactory(name="Tag 1")
        cls.tag_2 = TagFactory(name="Another tag")
        cls.quiz = QuizFactory(name="Mon premier quiz")  # tags=[cls.tag_1, cls.tag_2]
        cls.quiz.tags.set([cls.tag_1, cls.tag_2])
        cls.question_1 = QuestionFactory(text="Une question")
        cls.question_2 = QuestionFactory(text="Une autre question")
        QuizQuestion.objects.create(quiz=cls.quiz, question=cls.question_1, order=2)
        QuizQuestion.objects.create(quiz=cls.quiz, question=cls.question_2, order=1)

    def test_str(self):
        self.assertTrue(self.quiz.name in str(self.quiz))
        self.assertTrue(str(self.quiz.id) not in str(self.quiz))

    def test_slug_field(self):
        self.assertEqual(self.quiz.slug, "mon-premier-quiz")

    def test_question_count(self):
        self.assertEqual(self.quiz.question_count, 2)

    def test_questions_id_list(self):
        self.assertEqual(len(self.quiz.questions_id_list), 2)
        self.assertEqual(self.quiz.questions_id_list[0], self.question_1.id)

    def test_questions_id_list_with_order(self):
        self.assertEqual(len(self.quiz.questions_id_list_with_order), 2)
        self.assertEqual(self.quiz.questions_id_list_with_order[0], self.question_2.id)

    def test_tags_list(self):
        self.assertEqual(len(self.quiz.tags_list), 2)
        self.assertEqual(self.quiz.tags_list[0], self.tag_2.name)


class QuizModelSaveTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = UserFactory(first_name="Paul", last_name="Dupont")
        cls.tag_1 = TagFactory(name="Tag 1")
        cls.tag_2 = TagFactory(name="Another tag")
        cls.quiz = QuizFactory(name="Quiz 1")  # tags=[cls.tag_1, cls.tag_2], authors=[cls.user_1])
        cls.quiz.tags.set([cls.tag_1, cls.tag_2])
        cls.quiz.authors.set([cls.user_1])

    def test_update_related_flatten_fields_on_save(self):
        user_2 = UserFactory(first_name="Marie", last_name="Dupond")
        self.quiz.validator = user_2
        self.quiz.save()
        self.assertEqual(self.quiz.validator_string, user_2.full_name)

    def test_update_m2m_flatten_fields_on_save(self):
        # tags
        tag_3 = TagFactory(name="ABC")
        self.quiz.tags.add(tag_3)
        # self.quiz.save()  # no need to run save(), m2m_changed signal was triggered above
        self.assertEqual(self.quiz.tags.count(), 2 + 1)
        self.assertEqual(len(self.quiz.tag_list), 3)
        self.assertEqual(self.quiz.tag_list[0], tag_3.name)

    def test_update_m2m_through_flatten_fields_on_save(self):
        # authors
        user_2 = UserFactory(first_name="Marie", last_name="Dupond")
        QuizAuthor.objects.create(quiz=self.quiz, author=user_2)
        # self.quiz.save()  # no need to run save(), m2m_changed signal was triggered above
        self.assertEqual(self.quiz.authors.count(), 1 + 1)
        self.assertEqual(len(self.quiz.author_list), 2)
        self.assertEqual(len(self.quiz.authors_list), 2)
        self.assertEqual(self.quiz.author_list[0], self.user_1.full_name)

        # questions
        question_1 = QuestionFactory()
        QuizQuestion.objects.create(quiz=self.quiz, question=question_1, order=2)
        # self.quiz.save()  # no need to run save(), m2m_changed signal was triggered above
        self.assertEqual(self.quiz.questions.count(), 1)
        self.assertEqual(len(self.quiz.questions_id_list), 1)
        self.assertEqual(len(self.quiz.questions_id_list_with_order), 1)
        self.assertEqual(self.quiz.questions_id_list_with_order[0], question_1.id)
        question_2 = QuestionFactory()
        self.quiz.questions.add(question_2, through_defaults={"order": 1})
        # self.quiz.save()  # no need to run save(), m2m_changed signal was triggered above
        self.assertEqual(self.quiz.questions.count(), 2)
        self.assertEqual(len(self.quiz.questions_id_list), 2)
        self.assertEqual(len(self.quiz.questions_id_list_with_order), 2)
        self.assertEqual(self.quiz.questions_id_list_with_order[0], question_2.id)

        # relationships
        quiz_2 = QuizFactory(name="Un autre quiz")
        QuizRelationship.objects.create(from_quiz=self.quiz, to_quiz=quiz_2, status="suivant")
        # self.quiz.save()  # no need to run save(), m2m_changed signal was triggered above
        self.assertEqual(self.quiz.relationships.count(), 1)
        self.assertEqual(len(self.quiz.relationships_list), 1)
        self.assertEqual(self.quiz.relationships_list[0], f"{quiz_2.id} (suivant)")
        self.assertEqual(len(quiz_2.relationships_list), 1)
        self.assertEqual(quiz_2.relationships_list[0], f"{self.quiz.id} (précédent)")
        quiz_3 = QuizFactory(name="Quiz 3")
        QuizRelationship.objects.create(from_quiz=quiz_3, to_quiz=self.quiz, status="suivant")
        # self.quiz.save()  # no need to run save(), m2m_changed signal was triggered above
        self.assertEqual(self.quiz.relationships.count(), 1)  # Why not 2 ? symmetrical=False ?
        self.assertEqual(len(self.quiz.relationships_list), 2)
        self.assertEqual(self.quiz.relationships_list[1], f"{quiz_3.id} (précédent)")
        self.assertEqual(len(quiz_3.relationships_list), 1)
        self.assertEqual(quiz_3.relationships_list[0], f"{self.quiz.id} (suivant)")


class QuizModelHistoryTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tag_1 = TagFactory(name="Tag 1")
        cls.tag_2 = TagFactory(name="Another tag")
        cls.quiz = QuizFactory(name="Quiz 1")
        cls.quiz.tags.set([cls.tag_1, cls.tag_2])

    def test_history_object_on_create(self):
        self.assertEqual(self.quiz.history.count(), 1 + 1)
        create_history_item = self.quiz.history.last()
        self.assertEqual(create_history_item.history_type, "+")
        self.assertEqual(create_history_item.name, self.quiz.name)
        self.assertEqual(len(create_history_item.tag_list), 0)
        update_history_item = self.quiz.history.first()
        self.assertEqual(update_history_item.history_type, "~")
        self.assertEqual(update_history_item.name, self.quiz.name)
        self.assertEqual(len(update_history_item.tag_list), 2)
        self.assertEqual(update_history_item.history_changed_fields, ["tag_list"])

    def test_history_object_created_on_save(self):
        self.quiz.publish = True
        self.quiz.save()
        self.assertEqual(self.quiz.history.count(), 2 + 1)
        update_history_item = self.quiz.history.first()
        self.assertEqual(update_history_item.history_type, "~")
        self.assertEqual(update_history_item.history_changed_fields, ["publish"])

    def test_history_diff(self):
        self.quiz.name = "Le vrai nom"
        self.quiz.introduction = "Une introduction"
        self.quiz.conclusion = "Une conclusion"
        self.quiz.save()
        self.assertEqual(self.quiz.history.count(), 2 + 1)
        update_history_item = self.quiz.history.first()
        previous_history_item = self.quiz.history.first().prev_record
        delta = update_history_item.diff_against(previous_history_item)
        self.assertEqual(len(delta.changes), 3)
        CHANGE_FIELDS = ["name", "introduction", "conclusion"]
        delta_change_fields = [change.field for change in delta.changes]
        for field in CHANGE_FIELDS:
            self.assertTrue(field in delta_change_fields)
            self.assertTrue(field in update_history_item.history_changed_fields)


class QuizModelQuerySetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        QuizFactory(
            name="Quiz 1",
            validation_status=constants.VALIDATION_STATUS_VALIDATED,
            publish=True,
            visibility=constants.VISIBILITY_PUBLIC,
        )
        QuizFactory(
            name="Quiz 2",
            validation_status=constants.VALIDATION_STATUS_VALIDATED,
            publish=True,
            visibility=constants.VISIBILITY_HIDDEN,
        )
        QuizFactory(
            name="Quiz 3",
            validation_status=constants.VALIDATION_STATUS_VALIDATED,
            publish=True,
            visibility=constants.VISIBILITY_PRIVATE,
        )
        QuizFactory(
            name="Quiz 4",
            validation_status=constants.VALIDATION_STATUS_DRAFT,
            publish=False,
            visibility=constants.VISIBILITY_PUBLIC,
        )
        QuizFactory(
            name="Quiz 5",
            validation_status=constants.VALIDATION_STATUS_DRAFT,
            publish=False,
            visibility=constants.VISIBILITY_HIDDEN,
        )
        QuizFactory(
            name="Quiz 6",
            introduction="xyz",
            validation_status=constants.VALIDATION_STATUS_DRAFT,
            publish=False,
            visibility=constants.VISIBILITY_PRIVATE,
        )

    def test_question_validated(self):
        self.assertEqual(Quiz.objects.validated().count(), 3)

    def test_question_not_validated(self):
        self.assertEqual(Quiz.objects.not_validated().count(), 3)

    def test_quiz_published(self):
        self.assertEqual(Quiz.objects.published().count(), 3)

    def test_quiz_public(self):
        self.assertEqual(Quiz.objects.public().count(), 4)

    def test_quiz_public_published(self):
        self.assertEqual(Quiz.objects.public().published().count(), 2)

    def test_simple_search(self):
        self.assertEqual(Quiz.objects.simple_search(value="xy").count(), 1)


class QuizQuestionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(first_name="Paul", last_name="Dupont")
        cls.question = QuestionFactory(text="Une question")
        cls.quiz = QuizFactory(name="Quiz 1")  # questions=[cls.question]
        QuizQuestion.objects.create(quiz=cls.quiz, question=cls.question, order=1)

    def test_cannot_have_duplicate_quiz_question(self):
        self.assertRaises(ValidationError, QuizQuestion.objects.create, quiz=self.quiz, question=self.question)

    def test_cannot_add_question_with_same_order(self):
        question_2 = QuestionFactory(text="Une autre question")
        self.assertRaises(ValidationError, QuizQuestion.objects.create, quiz=self.quiz, question=question_2, order=1)


class QuizAuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(first_name="Paul", last_name="Dupont")
        cls.quiz = QuizFactory(name="Quiz 1")  # authors=[cls.user]
        cls.quiz.authors.set([cls.user])

    def test_cannot_have_duplicate_quiz_author(self):
        self.assertRaises(ValidationError, QuizAuthor.objects.create, quiz=self.quiz, author=self.user)
