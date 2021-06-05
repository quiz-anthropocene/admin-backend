import json
import requests

from django.conf import settings

from core.models import Configuration


def newsletter_registration(email):
    configuration = Configuration.get_solo()

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": settings.SIB_API_KEY,
    }

    data = {
        "email": email,
        # "attributes": {
        #     "FIRSTNAME": "",
        #     "LASTNAME": ""
        # },
        "includeListIds": [int(settings.SIB_NEWSLETTER_LIST_ID)],
        "templateId": int(settings.SIB_NEWSLETTER_DOI_TEMPLATE_ID),
        "redirectionUrl": configuration.application_frontend_url
        + "?newsletter=confirmed",
        "updateEnabled": True,
    }

    return requests.post(
        settings.SIB_CONTACT_DOI_ENDPOINT, headers=headers, data=json.dumps(data)
    )
