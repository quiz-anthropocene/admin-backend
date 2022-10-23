import factory

from users import constants
from users.models import User


DEFAULT_PASSWORD = "P4ssw0rd!*"


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Sequence("first_name{0}".format)
    last_name = factory.Sequence("last_name{0}".format)
    email = factory.Sequence("email{0}@example.com".format)
    password = factory.PostGenerationMethodCall("set_password", DEFAULT_PASSWORD)
    roles = [constants.USER_ROLE_CONTRIBUTOR]
