from django.test import TestCase
from django.urls import reverse

from users import constants
from users.factories import DEFAULT_PASSWORD, UserFactory


USER_URLS = ["users:home", "users:administrator_list"]


class UserViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()
        cls.user_super_contributor = UserFactory(roles=[constants.USER_ROLE_SUPER_CONTRIBUTOR])
        cls.user_admin = UserFactory(roles=[constants.USER_ROLE_ADMINISTRATOR])

    def test_anonymous_user_cannot_access_user_pages(self):
        for user_url in USER_URLS:
            url = reverse(user_url)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn("/accounts/login/?next=", response.url)

    def test_simple_user_cannot_access_user_pages(self):
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        for user_url in USER_URLS:
            url = reverse(user_url)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)

    def test_contributor_can_access_users_pages(self):
        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        for user_url in USER_URLS:
            url = reverse(user_url)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
