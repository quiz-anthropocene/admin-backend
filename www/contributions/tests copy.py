from django.test import TestCase
from django.urls import reverse

from contributions.factories import ContributionFactory
from users.factories import DEFAULT_PASSWORD, UserFactory


CONTRIBUTIONS_DETAIL_URLS = [
    "contributions:detail_view",
]


class ContributionListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()
        cls.contribution_1 = ContributionFactory()
        cls.contribution_2 = ContributionFactory()

    def test_anonymous_user_cannot_access_contribution_list(self):
        url = reverse("contributions:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/contributions/")

    def test_only_contributor_can_access_contribution_list(self):
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        url = reverse("contributions:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        url = reverse("contributions:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["contribution"]), 2)


class GlossaryItemDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.contribution_1 = ContributionFactory()
        cls.contribution_2 = ContributionFactory()

    def test_anonymous_user_cannot_access_contribution_detail(self):
        for edit_url in CONTRIBUTIONS_DETAIL_URLS:
            url = reverse(edit_url, args=[self.contribution_1.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_contributor_can_access_contribution_detail(self):
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        url = reverse("contributions:detail_view", args=[self.contribution_1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["contribution"].id, self.contribution_1.id)
