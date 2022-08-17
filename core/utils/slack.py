import json

import requests
from django.conf import settings


SLACK_BASE_URL = "https://hooks.slack.com/services/"
HEADERS = {}


def format_text(text):
    # https://api.slack.com/reference/surfaces/formatting
    text_formatted = text.replace("<i>", "_").replace("</i>", "_")
    text_formatted = text_formatted.replace("<strong>", "*").replace("</strong>", "*")
    return text_formatted


def send_message_to_channel(text: str, service_id: str):
    data = {"text": format_text(text)}

    if settings.DEBUG:
        return True

    try:
        response = requests.post(f"{SLACK_BASE_URL}{service_id}", headers=HEADERS, data=json.dumps(data))
        response.raise_for_status()
        # you'll receive a "HTTP 200" response with a plain text ok indicating that your message posted successfully
        return True
    except requests.exceptions.HTTPError as e:
        raise e
