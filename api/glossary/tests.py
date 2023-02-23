from django.test import TestCase
from django.urls import reverse

from core import constants
from glossary.factories import GlossaryItemFactory


class GlossaryApiTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        GlossaryItemFactory()
        GlossaryItemFactory(name="IPCC", language=constants.LANGUAGE_ENGLISH)

    def test_glossary_list(self):
        response = self.client.get(reverse("api:glossary-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data["results"], list)
        self.assertEqual(len(response.data["results"]), 2)

    def test_glossary_list_filter_by_language(self):
        response = self.client.get(reverse("api:glossary-list"), {"language": constants.LANGUAGE_ENGLISH})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
