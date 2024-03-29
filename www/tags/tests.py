from django.test import TestCase
from django.urls import reverse

from tags.factories import TagFactory
from tags.models import Tag
from users.factories import DEFAULT_PASSWORD, UserFactory


TAG_DETAIL_URLS = [
    "tags:detail_view",
    "tags:detail_edit",
    "tags:detail_questions",
    "tags:detail_quizs",
]

TAG_FORM_DEFAULT = {
    "name": "Tag 1",
}


class TagListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("tags:list")
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()
        cls.tag_1 = TagFactory(name="Tag 1")
        cls.tag_2 = TagFactory(name="Tag 2")

    def test_only_contributor_can_access_tag_list(self):
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
        self.assertEqual(len(response.context["tags"]), 2)


class TagDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.tag_1 = TagFactory(name="Tag 1")
        cls.tag_2 = TagFactory(name="Tag 2")

    def test_anonymous_user_cannot_access_tag_detail(self):
        for detail_url in TAG_DETAIL_URLS:
            url = reverse(detail_url, args=[self.tag_1.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn("/accounts/login/?next=", response.url)

    def test_contributor_can_access_tag_detail(self):
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        for detail_url in TAG_DETAIL_URLS:
            url = reverse(detail_url, args=[self.tag_1.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["tag"].id, self.tag_1.id)


class TagCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("tags:create")
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()

    def test_only_contributor_can_access_tag_create(self):
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

    def test_contributor_can_create_tag(self):
        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        response = self.client.post(self.url, data=TAG_FORM_DEFAULT)
        self.assertEqual(response.status_code, 302)  # 201
        self.assertEqual(Tag.objects.count(), 1)
