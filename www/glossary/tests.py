from django.test import TestCase
from django.urls import reverse

from glossary.factories import GlossaryItemFactory
from users.factories import DEFAULT_PASSWORD, UserFactory


class GlossaryListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()
        cls.glossary_item_1 = GlossaryItemFactory()
        cls.glossary_item_2 = GlossaryItemFactory()

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
