from datetime import date

import notion
from notion.client import NotionClient

from django.conf import settings

"""
Notion: connection
"""


def get_notion_client():
    # try:
    #     client = NotionClient(token_v2=settings.TOKEN_V2)
    # except Exception as e:
    #     # usually: 401 Client Error: Unauthorized for url: https://www.notion.so/api/v3/loadUserContent # noqa
    #     print(e)
    #     raise
    client = NotionClient(token_v2=settings.TOKEN_V2)
    return client


"""
Notion: get table
"""


def get_contribution_table(notion_client):
    # page = client.get_block(settings.CONTRIBUTION_PAGE_URL)
    table = notion_client.get_collection_view(settings.CONTRIBUTION_TABLE_URL)
    return table


"""
Notion: get current rows
"""

# get rows
# for row in table.collection.get_rows():
#     print(row, row.created)
#     if row.created:
#         print(row.created.start)


"""
Notion: add row
"""


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
    row.created = notion.collection.NotionDate(date.today())
    return row
