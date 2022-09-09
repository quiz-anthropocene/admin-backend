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


def send_message_to_slack_channel(text: str, service_id: str):
    data = {"text": format_text(text)}

    if not settings.DEBUG and not settings.TESTING:
        if not service_id:
            # raise Exception("send_message_to_slack_channel: service_id missing")
            return True
        try:
            response = requests.post(f"{SLACK_BASE_URL}{service_id}", headers=HEADERS, data=json.dumps(data))
            response.raise_for_status()
            # you'll receive a "HTTP 200" response with a plain text ok indicating that your message posted successfully  # noqa
            return True
        except requests.exceptions.HTTPError as e:
            raise e
    else:
        return True


def send_message_to_webhook(text: str, webhook_url: str):
    data = {"text": format_text(text)}

    if not settings.DEBUG and not settings.TESTING:
        if not webhook_url:
            # raise Exception("send_message_to_webhook: webhook_url missing")
            return True
        try:
            response = requests.post(webhook_url, headers=HEADERS, data=json.dumps(data))
            response.raise_for_status()
            # you'll receive a "HTTP 200" response with a plain text ok indicating that your message posted successfully  # noqa
            return True
        except requests.exceptions.HTTPError as e:
            raise e
    else:
        return True
