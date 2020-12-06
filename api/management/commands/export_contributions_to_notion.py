from django.utils import timezone
from django.conf import settings
from django.core.management import BaseCommand

from api import utilities_notion
from api.models import Configuration, Contribution


class Command(BaseCommand):
    """
    Usage:
    python manage.py export_contributions_to_notion
    """

    def handle(self, *args, **options):
        # init
        config = Configuration.get_solo()
        contributions_last_exported = config.notion_contributions_last_exported
        print("Contributions last exported:", contributions_last_exported)

        if contributions_last_exported:
            new_contributions_to_export = Contribution.objects.filter(
                created__gte=contributions_last_exported
            )
        else:
            new_contributions_to_export = Contribution.objects.all()
        print("New contributions found:", new_contributions_to_export.count())

        if not settings.DEBUG:
            try:
                for new_contribution in new_contributions_to_export:
                    utilities_notion.add_contribution_row(
                        contribution_text=new_contribution.text,
                        contribution_description=new_contribution.description,
                        contribution_type=new_contribution.type,
                    )

                # update config
                config = Configuration.get_solo()
                config.notion_contributions_last_exported = timezone.now()
                config.save()

            except Exception as e:
                Contribution.objects.create(text=e)
                self.stdout.write(str(e))
