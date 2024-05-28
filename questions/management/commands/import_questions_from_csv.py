import csv

from django.core.exceptions import ValidationError
from django.core.management import BaseCommand
from django.utils import translation

from core import constants
from questions.models import Question, QuestionRelationship
from quizs.models import Quiz, QuizQuestion


MODEL_FIELDS = [field.name for field in Question._meta.fields]
FIELDS_TO_IGNORE = ["id", "validation_status", "answer_image_url", "answer_video_url", "created_at", "updated_at"]

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
    pipenv run python manage.py import_questions_from_csv --file <file_path> --language <language> (--type <type>) [--dry-run]  # noqa
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
                if "category_id" in item:
                    item_create["category_id"] = int(item["category_id"])
                if "author_id" in item:
                    item_create["author_id"] = int(item["author_id"])

                try:
                    question = Question.objects.create(**item_create)
                    self.stdout.write(f"Question created: {question}")

                    if options["type"] == "traduction":
                        if "id" in item:
                            from_question = Question.objects.get(id=item["id"])
                            question_relationship = QuestionRelationship.objects.create(
                                from_question=from_question, to_question=question, status="traduction"
                            )
                            self.stdout.write(f"QuestionRelationship created: {question_relationship}")

                    if item["quiz_slug"]:
                        quiz = Quiz.objects.get(slug=item["quiz_slug"])
                        QuizQuestion.objects.create(quiz=quiz, question=question, order=item["quiz_question_order"])

                except ValidationError as e:
                    self.stdout.write(f"Error: {e}")
