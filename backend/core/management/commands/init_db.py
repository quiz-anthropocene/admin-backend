from io import StringIO

import yaml
from django.core.management import BaseCommand, call_command
from django.db import connection

from categories.models import Category
from core.models import Configuration
from core.utils import utilities
from glossary.models import GlossaryItem
from questions.models import Question
from quizs.models import Quiz, QuizQuestion, QuizRelationship
from tags.models import Tag


APP_NAME = "api"
CONFIGURATION_FILE_PATH = "../data/configuration.yaml"
CATEGORIES_FILE_PATH = "../data/categories.yaml"
TAGS_FILE_PATH = "../data/tags.yaml"
QUESTIONS_FILE_PATH = "../data/questions.yaml"
QUIZS_FILE_PATH = "../data/quizs.yaml"
QUIZ_QUESTIONS_FILE_PATH = "../data/quiz-questions.yaml"
QUIZ_RELATIONSHIPS_FILE_PATH = "../data/quiz-relationships.yaml"
GLOSSARY_FILE_PATH = "../data/ressources-glossaire.yaml"


class Command(BaseCommand):
    """
    Usage:
    python manage.py init_db
    python manage.py init_db --with-sql-reset
    """

    help = """Initialize database with the files in the /data folder"""

    MODELS_LIST = [
        # (Configuration, CONFIGURATION_FILE_PATH),
        (Category, CATEGORIES_FILE_PATH),
        (Tag, TAGS_FILE_PATH),
        (Question, QUESTIONS_FILE_PATH),
        (Quiz, QUIZS_FILE_PATH),
        (QuizQuestion, QUIZ_QUESTIONS_FILE_PATH),
        (QuizRelationship, QUIZ_RELATIONSHIPS_FILE_PATH),
        (GlossaryItem, GLOSSARY_FILE_PATH),
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            "--with-sql-reset",
            default=False,
            action="store_true",
            dest="with-sql-reset",
            help="Reset the SQL table sequences afterwards",
        )

    def handle(self, *args, **options):
        # delete + add data
        self.init_configuration_table()
        for model_item in self.MODELS_LIST:
            self.init_model_table(model_item[0], model_item[1])
        if options["with-sql-reset"]:
            # reset table indexes
            self.reset_sql_squences()

    def init_configuration_table(self):
        Configuration.objects.all().delete()
        configuration_file = open(CONFIGURATION_FILE_PATH, "r")
        configuration_data = yaml.safe_load(configuration_file)
        # only 1 configuration: configuration_data is a dict
        Configuration.objects.create(**configuration_data[0])
        print("Configuration:", Configuration.objects.count(), "object")

    def init_model_table(self, model, data_file_path):
        model.objects.all().delete()
        data_file = open(data_file_path, "r")
        data = yaml.safe_load(data_file)
        utilities.load_model_data_to_db(model, data)
        print(f"{model._meta.object_name}:", model.objects.count(), "objects")

    def reset_sql_squences(self):
        """
        https://docs.djangoproject.com/en/3.1/ref/django-admin/#sqlsequencereset
        https://stackoverflow.com/a/44113124
        """
        print("Resetting SQL sequences...")
        out = StringIO()
        call_command("sqlsequencereset", APP_NAME, stdout=out, no_color=True)
        sql = out.getvalue()
        with connection.cursor() as cursor:
            cursor.execute(sql)
        out.close()
        print("Done")
