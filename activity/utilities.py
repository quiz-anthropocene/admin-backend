from django.utils import timezone

from activity.models import Event
from core.utils.utilities import truncate_with_ellipsis
from users.models import User


def get_event_object_name(event_object, event_object_type):
    event_object_name = ""

    if event_object_type in ["QUESTION"]:
        event_object_name = event_object.text
    elif event_object_type in ["USER"]:
        event_object_name = event_object.full_name
    else:  # "QUIZ"
        event_object_name = event_object.name

    return truncate_with_ellipsis(event_object_name, 150)


def create_event(user: User, event_verb: str, event_object, created=timezone.now()):
    # init
    event_dict = {"created": created}

    # actor: id & name
    if user:
        event_dict["actor_id"] = user.id
        event_dict["actor_name"] = truncate_with_ellipsis(user.full_name, 150)

    # event_verb
    if event_verb:
        event_dict["event_verb"] = event_verb

    # event_object: id, type, name
    if event_object:
        event_dict["event_object_id"] = event_object.id
        event_dict["event_object_type"] = event_object._meta.model._meta.model_name.upper()
        event_dict["event_object_name"] = get_event_object_name(event_object, event_dict["event_object_type"])

    # create event
    Event.objects.create(**event_dict)
