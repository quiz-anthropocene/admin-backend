from django.test import TestCase
from django.urls import reverse

from users import constants
from users.factories import DEFAULT_PASSWORD, UserFactory


class ProfileViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("profile:home")
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()
        cls.user_super_contributor = UserFactory(roles=[constants.USER_ROLE_SUPER_CONTRIBUTOR])
        cls.user_admin = UserFactory(roles=[constants.USER_ROLE_ADMINISTRATOR])

    def test_only_contributor_can_access_profile(self):
        # anonymous
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/profile/")
        # simple user
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        # contributor
        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
