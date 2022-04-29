from django.test import TestCase
from django.urls import reverse

from tags.factories import TagFactory
from users.factories import DEFAULT_PASSWORD, UserFactory


TAG_DETAIL_URLS = [
    "tags:detail_view",
    "tags:detail_edit",
    "tags:detail_questions",
    "tags:detail_quizs",
]


class TagListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()
        cls.tag_1 = TagFactory(name="Tag 1")
        cls.tag_2 = TagFactory(name="Tag 2")

    def test_anonymous_user_cannot_access_tag_list(self):
        url = reverse("tags:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/tags/")

    def test_only_contributor_can_access_tag_list(self):
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        url = reverse("tags:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        url = reverse("tags:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["tags"]), 2)


class TagDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.tag_1 = TagFactory(name="Tag 1")
        cls.tag_2 = TagFactory(name="Tag 2")

    def test_anonymous_user_cannot_access_tag_detail(self):
        for edit_url in TAG_DETAIL_URLS:
            url = reverse(edit_url, args=[self.tag_1.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_contributor_can_access_tag_detail(self):
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        url = reverse("tags:detail_view", args=[self.tag_1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["tag"].id, self.tag_1.id)
