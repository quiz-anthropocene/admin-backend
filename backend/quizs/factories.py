import factory
from django.utils.text import slugify

from quizs.models import Quiz


class QuizFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Quiz

    name = "Le quiz"
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    publish = False
