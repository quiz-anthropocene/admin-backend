import factory

from contributions.models import Contribution


class ContributionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contribution

    text = "Une contribution"
