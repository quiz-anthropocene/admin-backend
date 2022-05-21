import factory

from glossary.models import GlossaryItem


class GlossaryItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GlossaryItem

    name = "Un mot"
    definition_short = "Une courte définition"
