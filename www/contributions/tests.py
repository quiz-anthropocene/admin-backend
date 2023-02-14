from django.test import TestCase
from django.urls import reverse

from contributions.factories import ContributionFactory
from contributions.models import Contribution
from core import constants
from users.factories import DEFAULT_PASSWORD, UserFactory


CONTRIBUTIONS_DETAIL_URLS = [
    "contributions:detail_view",
    "contributions:detail_edit",
    "contributions:detail_reply_create",
]


class ContributionListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("contributions:list")
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()
        cls.contribution_1 = ContributionFactory()
        cls.contribution_2 = ContributionFactory()

    def test_only_contributor_can_access_contribution_list(self):
        # anonmyous
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
        self.assertEqual(len(response.context["contributions"]), 2)


class ContributionDetailViewTest(TestCase):
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
            self.assertIn("/accounts/login/?next=", response.url)

    def test_contributor_can_access_contribution_detail(self):
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        url = reverse("contributions:detail_view", args=[self.contribution_1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["contribution"].id, self.contribution_1.id)


class ContributionEditViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()
        cls.contribution = ContributionFactory(status=constants.CONTRIBUTION_STATUS_PENDING)
        cls.contribution_with_reply = ContributionFactory()
        cls.contribution_reply = ContributionFactory(parent=cls.contribution_with_reply)

    def test_contributor_can_access_contribution_edit(self):
        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        url = reverse("contributions:detail_edit", args=[self.contribution.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_contributor_can_edit_contribution(self):
        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        url = reverse("contributions:detail_edit", args=[self.contribution.id])
        response = self.client.post(url, data={"status": constants.CONTRIBUTION_STATUS_PROCESSED})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Contribution.objects.get(id=self.contribution.id).status, constants.CONTRIBUTION_STATUS_PROCESSED
        )

    def test_contributor_cannot_access_contribution_with_reply_edit(self):
        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        url = reverse("contributions:detail_edit", args=[self.contribution_reply.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(f"/{self.contribution_with_reply.id}/", response.url)


class ContributionReplyCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()
        cls.contribution = ContributionFactory()
        cls.contribution_with_reply = ContributionFactory()
        cls.contribution_reply = ContributionFactory(parent=cls.contribution_with_reply)

    def test_contributor_can_access_contribution_reply_create(self):
        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        url = reverse("contributions:detail_reply_create", args=[self.contribution.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_contributor_can_create_reply_to_contribution(self):
        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        url = reverse("contributions:detail_reply_create", args=[self.contribution.id])
        response = self.client.post(url, data={"text": "Une réponse", "type": constants.CONTRIBUTION_TYPE_REPLY})
        self.assertEqual(response.status_code, 302)  # 201
        self.assertEqual(Contribution.objects.count(), 3 + 1)
        self.assertTrue(Contribution.objects.get(id=self.contribution.id).has_replies)

    def test_contributor_cannot_access_contribution_with_reply_reply_create(self):
        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        url = reverse("contributions:detail_reply_create", args=[self.contribution_reply.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(f"/{self.contribution_with_reply.id}/", response.url)
