from django.test import TestCase
from django.urls import reverse

from users import constants
from users.factories import DEFAULT_PASSWORD, UserFactory


PROFILE_DETAIL_URLS = [
    # "profile:home",
    "profile:info_view",
    "profile:info_card_view",
    "profile:info_card_create",
    # "profile:info_card_edit",
    "profile:questions_view",
    "profile:questions_stats",
    "profile:quizs_view",
    "profile:quizs_stats",
    "profile:history",
]


class ProfileViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("profile:home")
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()
        cls.user_super_contributor = UserFactory(roles=[constants.USER_ROLE_SUPER_CONTRIBUTOR])
        cls.user_admin = UserFactory(roles=[constants.USER_ROLE_ADMINISTRATOR])

    def test_only_contributor_can_access_profile_home(self):
        # anonymous
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/?next=", response.url)
        # simple user
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        # contributor
        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class ProfileDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def test_anonymous_user_cannot_access_profile_detail(self):
        for detail_url in PROFILE_DETAIL_URLS:
            url = reverse(detail_url)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn("/accounts/login/?next=", response.url)

    def test_contributor_can_access_profile_detail(self):
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        for detail_url in PROFILE_DETAIL_URLS:
            url = reverse(detail_url)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["user"].id, self.user.id)
