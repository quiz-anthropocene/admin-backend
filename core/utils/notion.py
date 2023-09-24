import json
from datetime import date, datetime

import requests
from django.conf import settings
from django.db.models.fields import URLField

from questions.models import Question


TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"  # "2021-05-05T13:02:00.000Z"  # milliseconds not managed
QUESTION_URL_FIELDS = [field.name for field in Question._meta.fields if type(field) is URLField]


# Official API

NOTION_API_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {settings.NOTION_API_SECRET}",
    "Notion-Version": f"{settings.NOTION_API_VERSION}",
}


def get_question_table_pages(sort_direction="descending", extra_data=None, start_cursor=None):
    """
    Retrive 100 pages from the question table
    """
    url = f"https://api.notion.com/v1/databases/{settings.NOTION_QUESTION_TABLE_ID}/query"
    data = {"sorts": [{"property": "Last edited time", "direction": sort_direction}]}
    if extra_data:
        data = {**data, **extra_data}
    if start_cursor:
        data["start_cursor"] = start_cursor

    response = requests.post(url, headers=NOTION_API_HEADERS, data=json.dumps(data))
    if response.status_code != 200:
        raise Exception(json.loads(response._content))

    return response


def create_page_in_database(database_id, page_properties):
    url = "https://api.notion.com/v1/pages"
    data = {
        "parent": {"database_id": database_id},
        "properties": page_properties,
    }

    response = requests.post(url, headers=NOTION_API_HEADERS, data=json.dumps(data))

    if response.status_code != 200:
        raise Exception(json.loads(response._content))

    return response


def update_page_properties(page_id, data={}):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    response = requests.patch(url, headers=NOTION_API_HEADERS, data=json.dumps(data))
    if response.status_code != 200:
        raise Exception(json.loads(response._content))

    return response


def process_page_properties(page_properties):
    """
    Fetch & cleanup fields
    """
    page_dict = dict()
    for key in page_properties:
        # Step 1: process key by Notion 'type"
        if page_properties[key]["type"] == "title":
            page_dict[key] = "".join([text["plain_text"] for text in page_properties[key]["title"]])
        elif page_properties[key]["type"] == "rich_text":
            page_dict[key] = "".join([text["plain_text"] for text in page_properties[key]["rich_text"]])  # noqa
        elif page_properties[key]["type"] == "number":
            page_dict[key] = page_properties[key]["number"]
        elif page_properties[key]["type"] == "select":
            try:
                page_dict[key] = page_properties[key]["select"]["name"]
            except (TypeError, AttributeError) as e:  # noqa
                page_dict[key] = ""
        elif page_properties[key]["type"] == "multi_select":
            page_dict[key] = [tag["name"] for tag in page_properties[key]["multi_select"]]
        elif page_properties[key]["type"] == "url":
            try:
                page_dict[key] = page_properties[key]["url"].strip()
            except (TypeError, AttributeError) as e:  # noqa
                page_dict[key] = ""
        elif page_properties[key]["type"] == "checkbox":
            page_dict[key] = page_properties[key]["checkbox"]  # True or False
        elif page_properties[key]["type"] == "date":
            try:
                page_dict[key] = page_properties[key]["date"]["start"]
            except (TypeError, AttributeError) as e:  # noqa
                page_dict[key] = ""
        elif page_properties[key]["type"] == "created_time":
            page_dict[key] = page_properties[key]["created_time"]
        elif page_properties[key]["type"] == "created_by":
            page_dict[key] = page_properties[key]["created_by"]
        elif page_properties[key]["type"] == "last_edited_by":
            page_dict[key] = page_properties[key]["last_edited_by"]
        elif page_properties[key]["type"] == "last_edited_time":
            page_dict[key] = page_properties[key]["last_edited_time"]
        else:
            raise Exception(f"process_page_properties: {page_properties[key]['type']} missing")

        # Step 2: process key by custom rules
        if key == "Text":
            page_dict["text"] = page_dict[key]
        if key == "difficulty":
            page_dict[key] = int(page_dict[key]) if page_dict[key] else None
        elif key == "added":
            page_dict[key] = (
                date.fromisoformat(page_dict[key])
                if page_dict[key]
                else datetime.strptime(page_dict["Created time"][:-5], TIMESTAMP_FORMAT).date()
            )  # noqa

    return page_dict
