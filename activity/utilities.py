from activity.models import Event
from users.models import User


def create_event(user: User, event_verb: str, event_object):
    # event_object_type
    event_object_type = event_object._meta.model._meta.verbose_name.upper()

    # event_object_name
    if event_object_type in ["QUESTION"]:
        event_object_name = event_object.text
    else:
        event_object_name = event_object.name

    # create event
    Event.objects.create(
        actor_id=user.id,
        actor_name=user.full_name,
        event_verb=event_verb,
        event_object_id=event_object.id,
        event_object_type=event_object_type,
        event_object_name=event_object_name,
    )
