import json

import requests
from django.conf import settings

from core.models import Configuration


HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "api-key": settings.SIB_API_KEY,
}


def add_to_contact_list(user, list_id=settings.SIB_CONTRIBUTOR_LIST_ID, extra_attributes=dict()):
    data = {
        "email": user.email,
        "listIds": [int(list_id)],
        "updateEnabled": True,
    }

    attributes = dict()
    if user.first_name:
        attributes["FIRSTNAME"] = user.first_name
    if user.last_name:
        attributes["LASTNAME"] = user.last_name
    if extra_attributes:
        attributes = {**attributes, **extra_attributes}
    data["attributes"] = attributes

    if settings.DEBUG:
        return True
    return requests.post(settings.SIB_CONTACT_ENDPOINT, headers=HEADERS, data=json.dumps(data))


def newsletter_registration(user_email):
    """
    Use Double-Opt-In Flow
    https://developers.sendinblue.com/reference/createdoicontact
    """
    configuration = Configuration.get_solo()

    data = {
        "email": user_email,
        # "attributes": {
        #     "FIRSTNAME": "",
        #     "LASTNAME": ""
        # },
        "includeListIds": [int(settings.SIB_NEWSLETTER_LIST_ID)],
        "templateId": int(settings.SIB_NEWSLETTER_DOI_TEMPLATE_ID),
        "redirectionUrl": configuration.application_frontend_url + "?newsletter=confirmed",
        "updateEnabled": True,
    }

    if settings.DEBUG:
        return True
    return requests.post(settings.SIB_CONTACT_DOI_ENDPOINT, headers=HEADERS, data=json.dumps(data))
