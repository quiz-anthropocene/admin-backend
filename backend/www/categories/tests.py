from django.test import TestCase
from django.urls import reverse

from categories.factories import CategoryFactory
from users.factories import DEFAULT_PASSWORD, UserFactory


CATEGORY_DETAIL_URLS = [
    "categories:detail_view",
    "categories:detail_edit",
    "categories:detail_questions",
]


class CategoryListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()
        cls.category_1 = CategoryFactory(name="Cat 1")
        cls.category_2 = CategoryFactory(name="Cat 2")

    def test_anonymous_user_cannot_access_category_list(self):
        url = reverse("categories:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/categories/")

    def test_only_contributor_can_access_category_list(self):
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        url = reverse("categories:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        url = reverse("categories:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["categories"]), 2)


class CategoryDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.category_1 = CategoryFactory(name="Cat 1")
        cls.category_2 = CategoryFactory(name="Cat 2")

    def test_anonymous_user_cannot_access_category_detail(self):
        for edit_url in CATEGORY_DETAIL_URLS:
            url = reverse(edit_url, args=[self.category_1.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_contributor_can_access_category_detail(self):
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        url = reverse("categories:detail_view", args=[self.category_1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["category"].id, self.category_1.id)
