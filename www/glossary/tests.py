from django.test import TestCase
from django.urls import reverse

from glossary.factories import GlossaryItemFactory
from glossary.models import GlossaryItem
from users.factories import DEFAULT_PASSWORD, UserFactory


GLOSSARY_ITEM_DETAIL_URLS = [
    "glossary:detail_view",
    "glossary:detail_edit",
    "glossary:detail_history",
]

GLOSSARY_ITEM_FORM_DEFAULT = {
    "name": "Mot 1",
    "definition_short": "Une définition",
}


class GlossaryListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("glossary:list")
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()
        cls.glossary_item_1 = GlossaryItemFactory(name="GIEC")
        cls.glossary_item_2 = GlossaryItemFactory(name="GES")

    def test_only_contributor_can_access_glossary_list(self):
        # anonymous
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/glossary/")
        # simple user
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        # contributor
        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        response = self.client.get(self.url)
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


class GlossaryItemCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("glossary:create")
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()

    def test_only_contributor_can_access_glossary_item_create(self):
        # anonymous
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))
        # simple user
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        # contributor
        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_contributor_can_create_glossary_item(self):
        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        response = self.client.post(self.url, data=GLOSSARY_ITEM_FORM_DEFAULT)
        self.assertEqual(response.status_code, 302)  # 201
        self.assertEqual(GlossaryItem.objects.count(), 1)
