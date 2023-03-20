from django.urls import reverse

from core import constants


def test_contribution(self):
    response = self.client.post(
        reverse("api:contribution-list"),
        data={"text": "du texte", "description": "une description", "type": constants.COMMENT_TYPE_LIST[0]},
    )
    self.assertEqual(response.status_code, 201)
    self.assertIsInstance(response.data, dict)
