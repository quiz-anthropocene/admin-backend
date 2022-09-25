from django.test import TestCase
from django.urls import reverse

from activity.models import Event
from users import constants as user_constants
from users.factories import DEFAULT_PASSWORD, UserFactory
from users.models import User


ADMIN_URLS = ["admin:home", "admin:contributor_list", "admin:contributor_create", "admin:history"]
CONTRIBUTOR_CREATE_FORM_DEFAULT = {
    "first_name": "First",
    "last_name": "Last",
    "email": "contributor@example.com",
    "roles": [user_constants.USER_ROLE_CONTRIBUTOR],
}


class ProfileAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_contributor = UserFactory()
        cls.user_super_contributor = UserFactory(roles=[user_constants.USER_ROLE_SUPER_CONTRIBUTOR])
        cls.user_admin = UserFactory(roles=[user_constants.USER_ROLE_ADMINISTRATOR])
        cls.user_contributor_admin = UserFactory(
            roles=[user_constants.USER_ROLE_CONTRIBUTOR, user_constants.USER_ROLE_ADMINISTRATOR]
        )

    def test_only_admin_can_access_admin_pages(self):
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


class ProfileAdminContributorCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_admin = UserFactory(roles=[user_constants.USER_ROLE_ADMINISTRATOR])

    def test_admin_can_create_quiz(self):
        self.client.login(email=self.user_admin.email, password=DEFAULT_PASSWORD)
        url = reverse("admin:contributor_create")
        response = self.client.post(url, data=CONTRIBUTOR_CREATE_FORM_DEFAULT)
        self.assertEqual(response.status_code, 302)  # 201
        self.assertEqual(User.objects.count(), 1 + 1)
        self.assertEqual(Event.objects.count(), 1)
