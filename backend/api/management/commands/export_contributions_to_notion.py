from datetime import datetime

from django.utils import timezone
from django.conf import settings
from django.core.management import BaseCommand

from core.models import Configuration
from api import utilities_notion
from api.models import Contribution


configuration = Configuration.get_solo()


class Command(BaseCommand):
    """
    Usage:
    python manage.py export_contributions_to_notion
    python manage.py export_contributions_to_notion --custom_start_date '2020-01-01 15:45'
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--custom_start_date",
            type=str,
            default=None,
            help="Set a custom start date. Format 'YYYY-MM-DD HH:MM'. Optional.",
        )

    def handle(self, *args, **options):
        # init date to filter from
        custom_start_date = options["custom_start_date"]
        if custom_start_date:
            custom_start_date_parsed = datetime.strptime(
                custom_start_date, "%Y-%m-%d %H:%M"
            )
            contributions_last_exported = timezone.make_aware(custom_start_date_parsed)
        else:
            contributions_last_exported = (
                configuration.notion_contributions_last_exported
            )
        print("Contributions last exported:", contributions_last_exported)

        # find new contributions
        if contributions_last_exported:
            new_contributions_to_export = Contribution.objects.filter(
                created__gte=contributions_last_exported
            )
        else:
            new_contributions_to_export = Contribution.objects.all()
        print("New contributions found:", new_contributions_to_export.count())

        # export new contributions to notion
        if not settings.DEBUG:
            try:
                for new_contribution in new_contributions_to_export:
                    new_contribution_properties = {
                        "text": {"title": [{"text": {"content": new_contribution.text}}]},
                        "type": {"select": {"name": new_contribution.type}},
                        "description": {"rich_text": [{"text": {"content": new_contribution.description}}]},  # noqa
                        "created": {"date": {"start": new_contribution.created.isoformat()}},
                    }
                    utilities_notion.create_page_in_database(settings.NOTION_CONTRIBUTION_TABLE_ID, new_contribution_properties)  # noqa

                # update configuration
                configuration.notion_contributions_last_exported = timezone.now()
                configuration.save()

                print("Done!")
                self.stdout.write(
                    f"New contributions exported: {new_contributions_to_export.count()}"
                )

            except Exception as e:
                print("Error !")
                Contribution.objects.create(text=e)
                self.stdout.write(str(e))
