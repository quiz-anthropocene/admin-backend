import factory
from django.utils.text import slugify

from core import constants
from quizs.models import Quiz


class QuizFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Quiz

    name = "Le quiz"
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    validation_status = constants.VALIDATION_STATUS_OK
    publish = False

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if extracted:
            # Add the iterable of groups using bulk addition
            self.tags.add(*extracted)

    @factory.post_generation
    def authors(self, create, extracted, **kwargs):
        if extracted:
            # Add the iterable of groups using bulk addition
            self.authors.add(*extracted)

    @factory.post_generation
    def questions(self, create, extracted, **kwargs):
        if extracted:
            # Add the iterable of groups using bulk addition
            self.questions.add(*extracted)
