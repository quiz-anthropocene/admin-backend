from django.test import TestCase
from django.urls import reverse

from users.factories import DEFAULT_PASSWORD, UserFactory
from users.models import User


class ProfileViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_contributor = UserFactory()
        cls.user_super_contributor = UserFactory(roles=[User.USER_ROLE_SUPER_CONTRIBUTOR])
        cls.user_admin = UserFactory(roles=[User.USER_ROLE_ADMINISTRATOR])

    def test_anonymous_user_cannot_access_profile(self):
        url = reverse("profile:home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/profile/")

    def test_user_can_access_profile(self):
        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        url = reverse("profile:home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_only_admin_user_has_admin_section(self):
        USERS_NOT_ALLOWED = [self.user_contributor, self.user_super_contributor]
        for user in USERS_NOT_ALLOWED:
            print(user.roles)
            self.client.login(email=user.email, password=DEFAULT_PASSWORD)
            url = reverse("profile:home")
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertNotContains(response, "Administration")

        self.client.login(email=self.user_admin.email, password=DEFAULT_PASSWORD)
        url = reverse("profile:home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Administration")


class ProfileAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_contributor = UserFactory()
        cls.user_super_contributor = UserFactory(roles=[User.USER_ROLE_SUPER_CONTRIBUTOR])
        cls.user_admin = UserFactory(roles=[User.USER_ROLE_ADMINISTRATOR])
        cls.user_contributor_admin = UserFactory(roles=[User.USER_ROLE_CONTRIBUTOR, User.USER_ROLE_ADMINISTRATOR])

    def test_only_admin_user_can_access_contributor_list(self):
        USERS_NOT_ALLOWED = [self.user_contributor, self.user_super_contributor]
        for user in USERS_NOT_ALLOWED:
            self.client.login(email=user.email, password=DEFAULT_PASSWORD)
            url = reverse("profile:admin_contributors")
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)

        USERS_ALLOWED = [self.user_admin, self.user_contributor_admin]
        for user in USERS_ALLOWED:
            self.client.login(email=self.user_admin.email, password=DEFAULT_PASSWORD)
            url = reverse("profile:admin_contributors")
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
