from datetime import datetime  # , date

import notion
from notion.client import NotionClient

from django.conf import settings

"""
Notion: connection
"""


def get_notion_client():
    # try:
    #     client = NotionClient(token_v2=settings.NOTION_TOKEN_V2)
    # except Exception as e:
    #     # usually: 401 Client Error: Unauthorized for url: https://www.notion.so/api/v3/loadUserContent # noqa
    #     print(e)
    #     raise
    client = NotionClient(token_v2=settings.NOTION_TOKEN_V2)
    return client


"""
Notion: Contribution page
- get table
- get current rows
- add row
"""


def get_contribution_table(notion_client):
    # page = client.get_block(settings.NOTION_CONTRIBUTION_PAGE_URL)
    table = notion_client.get_collection_view(settings.NOTION_CONTRIBUTION_TABLE_URL)
    return table


# get rows
# for row in table.collection.get_rows():
#     print(row, row.created)
#     if row.created:
#         print(row.created.start)


def add_contribution_row(
    contribution_text: str, contribution_description: str, contribution_type: str
):
    # init
    notion_client = get_notion_client()
    contribution_table = get_contribution_table(notion_client)
    # add row
    row = contribution_table.collection.add_row()
    row.type = contribution_type
    row.text = contribution_text
    row.description = contribution_description
    # row.created = notion.collection.NotionDate(date.today())
    row.created = notion.collection.NotionDate(datetime.now())
    return row


"""
Notion: Import stats page
- get table
- add row
"""


def get_import_stats_table(notion_client):
    # page = client.get_block(settings.NOTION_IMPORT_STATS_PAGE_URL)
    table = notion_client.get_collection_view(
        settings.NOTION_IMPORT_STATS_TABLE_URL + "coucou"
    )
    return table


def add_import_stats_row(total, new, update):
    # init
    notion_client = get_notion_client()
    import_stats_table = get_import_stats_table(notion_client)
    # add row
    row = import_stats_table.collection.add_row()
    row.action = "import"
    row.question_total = total
    row.question_new = new
    row.question_update = update
    row.date = notion.collection.NotionDate(datetime.now())
    return row
