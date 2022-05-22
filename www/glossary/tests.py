from django.test import TestCase
from django.urls import reverse

from glossary.factories import GlossaryItemFactory
from users.factories import DEFAULT_PASSWORD, UserFactory


GLOSSARY_ITEM_DETAIL_URLS = [
    "glossary:detail_view",
    "glossary:detail_edit",
    "glossary:detail_history",
]


class GlossaryListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()
        cls.glossary_item_1 = GlossaryItemFactory(name="GIEC")
        cls.glossary_item_2 = GlossaryItemFactory(name="GES")

    def test_anonymous_user_cannot_access_glossary_list(self):
        url = reverse("glossary:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/glossary/")

    def test_only_contributor_can_access_glossary_list(self):
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        url = reverse("glossary:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        url = reverse("glossary:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["glossary"]), 2)


class GlossaryItemDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.glossary_item_1 = GlossaryItemFactory(name="GIEC")
        cls.glossary_item_2 = GlossaryItemFactory(name="GES")

    def test_anonymous_user_cannot_access_glossary_item_detail(self):
        for edit_url in GLOSSARY_ITEM_DETAIL_URLS:
            url = reverse(edit_url, args=[self.glossary_item_1.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_contributor_can_access_glossary_item_detail(self):
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        url = reverse("glossary:detail_view", args=[self.glossary_item_1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["glossary_item"].id, self.glossary_item_1.id)
