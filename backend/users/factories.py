import factory

from users.models import User


DEFAULT_PASSWORD = "P4ssw0rd!*"


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Sequence("first_name{0}".format)
    last_name = factory.Sequence("last_name{0}".format)
    email = factory.Sequence("email{0}@example.com".format)
    password = factory.PostGenerationMethodCall("set_password", DEFAULT_PASSWORD)

    @factory.post_generation
    def questions(self, create, extracted, **kwargs):
        if extracted:
            # Add the iterable of groups using bulk addition
            self.questions.add(*extracted)

    @factory.post_generation
    def quizs(self, create, extracted, **kwargs):
        if extracted:
            # Add the iterable of groups using bulk addition
            self.quizs.add(*extracted)