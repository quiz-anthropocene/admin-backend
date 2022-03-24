from datetime import date, datetime

import yaml
from django.core.management import BaseCommand

from api import utilities_notion
from api.models import Glossary


class Command(BaseCommand):
    """
    Usage:
    - python manage.py notion_glossary_to_yaml
    - python manage.py notion_glossary_to_yaml --flat
    """

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            "--flat",
            default=False,
            action="store_true",
            dest="flat",
            help="Store items flat (without fields object)",
        )

    def handle(self, *args, **kwargs):
        # --- init
        id_counter = 1
        glossary_model_fields = [
            f.name for f in Glossary._meta.get_fields() if f.name not in ["id"]
        ]  # "created", "updated"
        notion_glossary_list = utilities_notion.get_glossary_rows()
        # print(list(map(lambda x: x['slug'], notion_glossary_table.collection.get_schema_properties()))) # noqa

        # --- glossary list
        glossary_list = list()
        for row in notion_glossary_list:
            glossary_item_base = dict()
            glossary_item_base["model"] = "api.glossary"
            glossary_item_base["pk"] = id_counter
            glossary_item_fields = dict()
            for field in glossary_model_fields:
                if field == "added":
                    glossary_item_fields[field] = datetime.date(row.get_property(field))
                # elif field == "name_alternatives":
                #     glossary_item_fields[field] = row.get_property(field).split(", ") if row.get_property(field) else "" # noqa
                elif field == "created" or field == "updated":
                    glossary_item_fields[field] = date.today()
                else:
                    glossary_item_fields[field] = row.get_property(field)
            if kwargs.get("flat"):
                glossary_list.append({**{"id": id_counter}, **glossary_item_fields})
            else:
                glossary_item_base["fields"] = glossary_item_fields
                glossary_list.append(glossary_item_base)
            id_counter += 1

        # --- write to file
        with open("data/ressources-glossaire.yaml", "w") as file:
            print(f"Glossary items: {len(glossary_list)}")
            yaml.safe_dump(
                glossary_list, file, allow_unicode=True, sort_keys=False
            )  # , explicit_start=False, explicit_end=False
