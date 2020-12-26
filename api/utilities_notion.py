from datetime import datetime  # , date

import notion  # https://github.com/jamalex/notion-py
from notion.client import NotionClient

from django.conf import settings


def get_notion_client():
    """
    Connection
    """
    # try:
    #     client = NotionClient(token_v2=settings.NOTION_TOKEN_V2)
    # except Exception as e:
    #     # usually: 401 Client Error: Unauthorized for url: https://www.notion.so/api/v3/loadUserContent # noqa
    #     print(e)
    #     raise
    client = NotionClient(token_v2=settings.NOTION_TOKEN_V2)
    return client


def get_questions_table():
    """
    Questions page: get table
    """
    notion_client = get_notion_client()
    # page = client.get_block(settings.NOTION_QUESTIONS_PAGE_URL)
    table = notion_client.get_collection_view(settings.NOTION_QUESTIONS_TABLE_URL)
    return table


def get_questions_table_rows():
    """
    Questions page: get current rows
    """
    questions_table = get_questions_table()
    rows = questions_table.collection.get_rows()
    return rows


def get_contribution_table():
    """
    Contribution page: get table
    """
    notion_client = get_notion_client()
    # page = client.get_block(settings.NOTION_CONTRIBUTION_PAGE_URL)
    table = notion_client.get_collection_view(settings.NOTION_CONTRIBUTION_TABLE_URL)
    return table


def add_contribution_row(
    contribution_text: str,
    contribution_description: str,
    contribution_type: str,
    contribution_date=datetime.now(),
):
    """
    Contribution page: add row
    """
    # init
    contribution_table = get_contribution_table()
    # add row
    row = contribution_table.collection.add_row()
    row.type = contribution_type
    row.text = contribution_text
    row.description = contribution_description
    # row.created = notion.collection.NotionDate(date.today())
    row.created = notion.collection.NotionDate(contribution_date)
    return row


def get_import_stats_table():
    """
    Import stats page: get table
    """
    notion_client = get_notion_client()
    # page = client.get_block(settings.NOTION_IMPORT_STATS_PAGE_URL)
    table = notion_client.get_collection_view(
        settings.NOTION_IMPORT_STATS_TABLE_URL + "coucou"
    )
    return table


def add_import_stats_row(total, new, update):
    """
    Import stats page: add row
    """
    # init
    import_stats_table = get_import_stats_table()
    # add row
    row = import_stats_table.collection.add_row()
    row.action = "import"
    row.question_total = total
    row.question_new = new
    row.question_update = update
    row.date = notion.collection.NotionDate(datetime.now())
    return row


def get_glossary_table():
    """
   Glossary page: get table
    """
    notion_client = get_notion_client()
    # page = client.get_block(settings.NOTION_GLOSSARY_PAGE_URL)
    table = notion_client.get_collection_view(settings.NOTION_GLOSSARY_TABLE_URL)
    return table


def get_glossary_rows():
    """
   Glossary page: get current rows
    """
    glossary_table = get_glossary_table()
    # sort_params = [{
    #     "property": "name",
    #     "direction": "descending",
    # }]
    # glossary_table_sorted = glossary_table.build_query(sort=sort_params).execute()
    rows = glossary_table.collection.get_rows()
    return rows
