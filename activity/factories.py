import factory

from activity.models import Event


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event
