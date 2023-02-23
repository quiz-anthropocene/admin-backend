from django.test import TestCase
from django.urls import reverse

from core import constants
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
    "language": constants.LANGUAGE_FRENCH,
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
        self.assertIn("/accounts/login/?next=", response.url)
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
        for detail_url in GLOSSARY_ITEM_DETAIL_URLS:
            url = reverse(detail_url, args=[self.glossary_item_1.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn("/accounts/login/?next=", response.url)

    def test_contributor_can_access_glossary_item_detail(self):
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        for detail_url in GLOSSARY_ITEM_DETAIL_URLS:
            url = reverse(detail_url, args=[self.glossary_item_1.id])
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
        self.assertIn("/accounts/login/?next=", response.url)
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
