from django.urls import reverse

from glossary.models import GlossaryItem


def test_glossary(self):
    GlossaryItem.objects.create(name="Anthropocène")
    response = self.client.get(reverse("api:glossary-list"))
    self.assertEqual(response.status_code, 200)
    self.assertIsInstance(response.data["results"], list)
    self.assertEqual(len(response.data["results"]), 1)
