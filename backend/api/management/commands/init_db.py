import yaml

from django.core.management import BaseCommand

from api import utilities
from api.models import (
    Configuration,
    Category,
    Tag,
    Question,
    Quiz,
    QuizRelationship,
    Glossary,
)


CONFIGURATION_FILE_PATH = "data/configuration.yaml"
CATEGORIES_FILE_PATH = "data/categories.yaml"
TAGS_FILE_PATH = "data/tags.yaml"
QUESTIONS_FILE_PATH = "data/questions.yaml"
QUIZZES_FILE_PATH = "data/quizzes.yaml"
QUIZ_RELATIONSHIPS_FILE_PATH = "data/quiz-relationships.yaml"
GLOSSARY_FILE_PATH = "data/ressources-glossaire.yaml"


class Command(BaseCommand):
    """
    Usage:
    python manage.py init_db
    """

    help = """Initialize database with the files in the /data folder"""

    MODELS_LIST = [
        (Category, CATEGORIES_FILE_PATH),
        (Tag, TAGS_FILE_PATH),
        (Question, QUESTIONS_FILE_PATH),
        (Quiz, QUIZZES_FILE_PATH),
        (QuizRelationship, QUIZ_RELATIONSHIPS_FILE_PATH),
        (Glossary, GLOSSARY_FILE_PATH),
    ]

    def handle(self, *args, **options):
        self.init_configuration_table()
        for model_item in self.MODELS_LIST:
            self.init_model_table(model_item[0], model_item[1])

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
