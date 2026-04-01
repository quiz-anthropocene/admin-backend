from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token

from users import constants
from users.factories import UserFactory


class TokenAuthenticationTest(TestCase):
    """
    Verifies that DRF token authentication works for administrator users.

    To generate a token for an existing admin from the CLI, run:
        python manage.py drf_create_token <email>
    """

    @classmethod
    def setUpTestData(cls):
        cls.admin_user = UserFactory(
            email="admin@example.com",
            roles=[constants.USER_ROLE_ADMINISTRATOR],
            is_staff=True,
        )
        cls.token, _ = Token.objects.get_or_create(user=cls.admin_user)

    def test_token_is_created_for_admin(self):
        self.assertIsNotNone(self.token.key)
        self.assertEqual(self.token.user, self.admin_user)

    def test_authenticated_request_with_token(self):
        """A valid token in the Authorization header grants access to the API."""
        url = reverse("api:question-list")
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Token {self.token.key}")
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_request_still_allowed(self):
        """Public API endpoints remain accessible without a token."""
        url = reverse("api:question-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
