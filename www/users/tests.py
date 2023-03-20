from django.test import TestCase
from django.urls import reverse

from users import constants
from users.factories import DEFAULT_PASSWORD, UserFactory
from users.models import UserCard


USER_URLS = ["users:home", "users:author_card_list", "users:administrator_list"]


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


class UserCardListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()
        cls.user_super_contributor = UserFactory(roles=[constants.USER_ROLE_SUPER_CONTRIBUTOR])
        UserCard.objects.create(user=cls.user_super_contributor, short_biography="A short biography")
        cls.user_admin = UserFactory(roles=[constants.USER_ROLE_ADMINISTRATOR])

    def test_contributor_can_access_user_card_list_page(self):
        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        url = reverse("users:author_card_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user_super_contributor.full_name)


class AdministratorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()
        cls.user_super_contributor = UserFactory(roles=[constants.USER_ROLE_SUPER_CONTRIBUTOR])
        cls.user_admin_1 = UserFactory(roles=[constants.USER_ROLE_ADMINISTRATOR])
        cls.user_admin_2 = UserFactory(roles=[constants.USER_ROLE_ADMINISTRATOR])

    def test_contributor_can_access_administrator_list_page(self):
        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        url = reverse("users:administrator_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        for user_admin in [self.user_admin_1, self.user_admin_2]:
            self.assertContains(response, user_admin.email)
