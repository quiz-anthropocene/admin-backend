from django.test import TestCase
from django.urls import reverse

from users import constants
from users.factories import DEFAULT_PASSWORD, UserFactory


ADMIN_URLS = ["admin:home", "admin:contributors", "admin:history"]


class ProfileAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_contributor = UserFactory()
        cls.user_super_contributor = UserFactory(roles=[constants.USER_ROLE_SUPER_CONTRIBUTOR])
        cls.user_admin = UserFactory(roles=[constants.USER_ROLE_ADMINISTRATOR])
        cls.user_contributor_admin = UserFactory(
            roles=[constants.USER_ROLE_CONTRIBUTOR, constants.USER_ROLE_ADMINISTRATOR]
        )

    def test_only_admin_user_can_access_admin_pages(self):
        USERS_NOT_ALLOWED = [self.user_contributor, self.user_super_contributor]
        for user in USERS_NOT_ALLOWED:
            for admin_url in ADMIN_URLS:
                self.client.login(email=user.email, password=DEFAULT_PASSWORD)
                url = reverse(admin_url)
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)

        USERS_ALLOWED = [self.user_admin, self.user_contributor_admin]
        for user in USERS_ALLOWED:
            for admin_url in ADMIN_URLS:
                self.client.login(email=self.user_admin.email, password=DEFAULT_PASSWORD)
                url = reverse(admin_url)
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
