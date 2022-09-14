from django.test import TestCase

from core import constants
from questions.factories import QuestionFactory
from quizs.factories import QuizFactory
from users import constants as user_constants
from users.factories import UserFactory
from users.models import User


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(first_name="First", last_name="Last", email="test@example.com")
        QuestionFactory(author=cls.user)
        QuestionFactory(author=cls.user)
        cls.quiz = QuizFactory(author=cls.user)
        cls.quiz.authors.set([cls.user])

    def test_str(self):
        self.assertEqual(str(self.user), "First Last")

    def test_full_name(self):
        self.assertEqual(self.user.full_name, "First Last")

    def test_question_count(self):
        self.assertEqual(self.user.question_count, 2)

    def test_quiz_count(self):
        self.assertEqual(self.user.quiz_count, 1)

    def test_has_question(self):
        self.assertTrue(self.user.has_question)


class UserModelRoleTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()
        cls.user_contributor_2 = UserFactory()
        cls.user_super_contributor = UserFactory(roles=[user_constants.USER_ROLE_SUPER_CONTRIBUTOR])
        cls.user_super_contributor_2 = UserFactory(
            roles=[user_constants.USER_ROLE_CONTRIBUTOR, user_constants.USER_ROLE_SUPER_CONTRIBUTOR]
        )
        cls.user_admin = UserFactory(roles=[user_constants.USER_ROLE_ADMINISTRATOR])
        cls.user_admin_2 = UserFactory(
            roles=[user_constants.USER_ROLE_SUPER_CONTRIBUTOR, user_constants.USER_ROLE_ADMINISTRATOR]
        )
        cls.user_admin_3 = UserFactory(
            roles=[user_constants.USER_ROLE_CONTRIBUTOR, user_constants.USER_ROLE_ADMINISTRATOR]
        )

    def test_has_role_contributor(self):
        self.assertFalse(self.user.has_role_contributor)
        self.assertTrue(self.user_contributor.has_role_contributor)
        self.assertTrue(self.user_super_contributor.has_role_contributor)
        self.assertTrue(self.user_admin.has_role_contributor)

    def test_has_role_super_contributor(self):
        self.assertFalse(self.user.has_role_super_contributor)
        self.assertFalse(self.user_contributor.has_role_super_contributor)
        self.assertTrue(self.user_super_contributor.has_role_super_contributor)
        self.assertTrue(self.user_admin.has_role_super_contributor)

    def test_has_role_super_admin(self):
        self.assertFalse(self.user.has_role_administrator)
        self.assertFalse(self.user_contributor.has_role_administrator)
        self.assertFalse(self.user_super_contributor.has_role_administrator)
        self.assertTrue(self.user_admin.has_role_administrator)

    def test_all_contributors(self):
        self.assertEqual(User.objects.all_contributors().count(), 2 + 2 + 3)

    def test_all_super_contributors(self):
        self.assertEqual(User.objects.all_super_contributors().count(), 2 + 3)

    def test_all_administrators(self):
        self.assertEqual(User.objects.all_administrators().count(), 3)


class UserModelQuerysetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = UserFactory(email="xyz@email.com", roles=[])
        cls.user_2 = UserFactory()
        cls.user_3 = UserFactory()
        QuestionFactory(author=cls.user_2)
        QuestionFactory(author=cls.user_2)
        QuestionFactory(author=cls.user_3, visibility=constants.VISIBILITY_PRIVATE)
        cls.quiz_1 = QuizFactory(name="quiz 1", author=cls.user_2)
        cls.quiz_1.authors.set([cls.user_2])
        cls.quiz_2 = QuizFactory(name="quiz 2", author=cls.user_3, visibility=constants.VISIBILITY_PRIVATE)
        cls.quiz_2.authors.set([cls.user_3])

    def test_has_question(self):
        self.assertEqual(User.objects.has_question().count(), 2)

    def test_has_quiz_old(self):
        self.assertEqual(User.objects.has_quiz_old().count(), 2)

    def test_has_quiz(self):
        self.assertEqual(User.objects.has_quiz().count(), 2)

    def test_has_public_content(self):
        self.assertEqual(User.objects.has_public_content().count(), 1)

    def test_simple_search(self):
        self.assertEqual(User.objects.simple_search(value="xy").count(), 1)
