from django.utils import timezone

from activity.models import Event
from users.models import User


def create_event(user: User, event_verb: str, event_object, created=timezone.now()):
    # actor_name
    actor_name = user.full_name
    if len(actor_name) > 150:
        actor_name = actor_name[:147] + "..."

    # event_object_type
    event_object_type = event_object._meta.model._meta.model_name.upper()

    # event_object_name
    if event_object_type in ["QUESTION"]:
        event_object_name = event_object.text
    elif event_object_type in ["USER"]:
        event_object_name = event_object.full_name
    else:
        event_object_name = event_object.name
    if len(event_object_name) > 150:
        event_object_name = event_object_name[:147] + "..."

    # create event
    Event.objects.create(
        actor_id=user.id,
        actor_name=actor_name,
        event_verb=event_verb,
        event_object_id=event_object.id,
        event_object_type=event_object_type,
        event_object_name=event_object_name,
        created=created,
    )
