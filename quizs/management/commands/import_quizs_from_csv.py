import csv

from django.core.exceptions import ValidationError
from django.core.management import BaseCommand
from django.utils import translation

from core import constants
from quizs.models import Quiz, QuizRelationship
from users.models import User


MODEL_FIELDS = [field.name for field in Quiz._meta.fields]
FIELDS_TO_IGNORE = ["id", "validation_status", "created_at", "updated_at"]

# we set the default language to English (for the name of the CSV columns)
translation.activate("en")


def read_csv(file_path):
    row_list = list()

    with open(file_path) as csv_file:
        csvreader = csv.DictReader(csv_file, delimiter=",")
        for index, row in enumerate(csvreader):
            row_list.append(row)

    return row_list


class Command(BaseCommand):
    """
    Usage:
    pipenv run python manage.py import_quizs_from_csv --file <file_path> --language <language> (--type <type>) [--dry-run]  # noqa
    """

    def add_arguments(self, parser):
        parser.add_argument("--file", type=str, required=True)
        parser.add_argument("--language", type=str, choices=constants.LANGUAGE_CHOICE_LIST, required=True)
        parser.add_argument("--type", type=str, choices=["traduction"])
        parser.add_argument("--dry-run", dest="dry_run", action="store_true", help="Dry run (no changes to the DB)")

    def handle(self, *args, **options):
        item_list = read_csv(options["file"])
        self.stdout.write("-" * 80)
        self.stdout.write(f"File row count: {len(item_list)}")

        file_header = list(item_list[0].keys())
        self.stdout.write(f"Header: {file_header}")

        for index, item in enumerate(item_list):
            self.stdout.write("-" * 80)
            self.stdout.write(f"Reading row: {index}")

            if not options["dry_run"]:
                item_create = {key: value for key, value in item.items() if key in MODEL_FIELDS}
                item_create = {key: value for key, value in item_create.items() if key not in FIELDS_TO_IGNORE}
                item_create["language"] = options["language"]

                try:
                    quiz = Quiz.objects.create(**item_create)
                    self.stdout.write(f"Quiz created: {quiz}")

                    if "author_id" in item:
                        user = User.objects.get(id=item["author_id"])
                        quiz.authors.add(user)

                    if options["type"] == "traduction":
                        if "id" in item:
                            from_quiz = Quiz.objects.get(id=item["id"])
                            quiz_relationship = QuizRelationship.objects.create(
                                from_quiz=from_quiz, to_quiz=quiz, status="traduction"
                            )
                            self.stdout.write(f"QuizRelationship created: {quiz_relationship}")

                except ValidationError as e:
                    self.stdout.write(f"Error: {e}")
