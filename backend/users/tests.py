from django.test import TestCase

from users import constants
from users.factories import UserFactory
from users.models import User


class UserModelTest(TestCase):
    def test_str(self):
        user = UserFactory(first_name="First", last_name="Last", email="test@example.com")
        self.assertEqual(str(user), "First Last")

    def test_full_name(self):
        user = UserFactory(first_name="First", last_name="Last", email="test@example.com")
        self.assertEqual(user.full_name, "First Last")


class UserRoleTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()
        cls.user_contributor_2 = UserFactory()
        cls.user_super_contributor = UserFactory(roles=[constants.USER_ROLE_SUPER_CONTRIBUTOR])
        cls.user_super_contributor_2 = UserFactory(
            roles=[constants.USER_ROLE_CONTRIBUTOR, constants.USER_ROLE_SUPER_CONTRIBUTOR]
        )
        cls.user_admin = UserFactory(roles=[constants.USER_ROLE_ADMINISTRATOR])
        cls.user_admin_2 = UserFactory(
            roles=[constants.USER_ROLE_SUPER_CONTRIBUTOR, constants.USER_ROLE_ADMINISTRATOR]
        )
        cls.user_admin_3 = UserFactory(roles=[constants.USER_ROLE_CONTRIBUTOR, constants.USER_ROLE_ADMINISTRATOR])

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
        self.assertFalse(self.user.has_role_admin)
        self.assertFalse(self.user_contributor.has_role_admin)
        self.assertFalse(self.user_super_contributor.has_role_admin)
        self.assertTrue(self.user_admin.has_role_admin)

    def test_all_contributors(self):
        self.assertEqual(User.objects.all_contributors().count(), 2 + 2 + 3)

    def test_all_super_contributors(self):
        self.assertEqual(User.objects.all_super_contributors().count(), 2 + 3)

    def test_all_administrators(self):
        self.assertEqual(User.objects.all_administrators().count(), 3)
