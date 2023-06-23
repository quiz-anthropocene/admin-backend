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

    if not settings.DEBUG and not settings.TESTING:
        return requests.post(settings.SIB_CONTACT_ENDPOINT, headers=HEADERS, data=json.dumps(data))
    else:
        print("Sendinblue: user not added to contact list (DEBUT or TESTING environment detected)")
        return True


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

    if not settings.DEBUG and not settings.TESTING:
        return requests.post(settings.SIB_CONTACT_DOI_ENDPOINT, headers=HEADERS, data=json.dumps(data))
    else:
        print("Sendinblue: user not registered to the newsletter (DEBUT or TESTING environment detected)")
        return True


def send_transactional_email_with_template_id(
    to_email,
    to_name,
    template_id,
    parameters=None,
    from_email=settings.DEFAULT_FROM_EMAIL,
    from_name=settings.DEFAULT_FROM_NAME,
):
    data = {
        "sender": {"email": from_email, "name": from_name},  # email must be a sender registered and verified in Brevo
        "to": [{"email": to_email, "name": to_name}],
        "templateId": template_id,
    }
    if parameters:
        data["params"] = parameters

    if not settings.DEBUG and not settings.TESTING:
        return requests.post(settings.SIB_SMTP_ENDPOINT, headers=HEADERS, data=json.dumps(data))
    else:
        print("Sendinblue: email not sent (DEBUT or TESTING environment detected)")
        return True


def send_transactional_email_with_html(
    to_email,
    to_name,
    subject,
    html,
    parameters=None,
    from_email=settings.DEFAULT_FROM_EMAIL,
    from_name=settings.DEFAULT_FROM_NAME,
):
    data = {
        "sender": {"email": from_email, "name": from_name},  # email must be a sender registered and verified in Brevo
        "to": [{"email": to_email, "name": to_name}],
        "subject": subject,
        "htmlContent": html,
    }
    if parameters:
        data["params"] = parameters

    if not settings.DEBUG and not settings.TESTING:
        return requests.post(settings.SIB_SMTP_ENDPOINT, headers=HEADERS, data=json.dumps(data))
    else:
        print("Sendinblue: email not sent (DEBUT or TESTING environment detected)")
        return True
