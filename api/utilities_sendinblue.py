import json
import requests

from django.conf import settings


def newsletter_registration(email):
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
        "redirectionUrl": settings.DOMAIN_URL,
        "updateEnabled": True,
    }

    return requests.post(
        settings.SIB_CONTACT_DOI_ENDPOINT, headers=headers, data=json.dumps(data)
    )
