import requests
from django.core.management import BaseCommand

from questions.models import Question
from quizs.models import Quiz


QUESTION_URL_FIELDS = Question.QUESTION_URL_FIELDS + Question.QUESTION_IMAGE_URL_FIELDS
QUIZ_URL_FIELDS = Quiz.QUIZ_URL_FIELDS + Quiz.QUIZ_IMAGE_URL_FIELDS
# GLOSSARY_ITEM_URL_FIELDS = GlossaryItem.GLOSSARY_ITEM_URL_FIELDS
# USER_CARD_URL_FIELDS =


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("=== detect_broken_links running")

        error_list = list()

        question_error_list = self.detect_question_broken_links()
        error_list.extend(question_error_list)
        quiz_error_list = self.detect_quiz_broken_links()
        error_list.extend(quiz_error_list)

    def detect_question_broken_links(self):
        error_list = list()
        progress = 0
        questions = Question.objects.all()
        print(f"=== Questions: {questions.count()}")

        for object in questions:
            for object_url_field in QUESTION_URL_FIELDS:
                url = getattr(object, object_url_field)
                if url:
                    try:
                        requests.get(url, timeout=10)
                    except Exception:
                        error_list.append(
                            {
                                "object_type": "Question",
                                "object_id": object.id,
                                "object_field_name": object_url_field,
                                "object_field_url": url,
                            }
                        )
            progress += 1
            if (progress % 100) == 0:
                print(f"{progress}...")

        print(f"Questions done. Found {len(error_list)} errors")
        return error_list

    def detect_quiz_broken_links(self):
        error_list = list()
        progress = 0
        quizs = Quiz.objects.all()
        print(f"=== Quizs: {quizs.count()}")

        for object in quizs:
            for object_url_field in QUIZ_URL_FIELDS:
                url = getattr(object, object_url_field)
                if url:
                    try:
                        requests.get(url, timeout=10)
                    except Exception:
                        error_list.append(
                            {
                                "object_type": "Quiz",
                                "object_id": object.id,
                                "object_field_name": object_url_field,
                                "object_field_url": url,
                            }
                        )
            progress += 1
            if (progress % 10) == 0:
                print(f"{progress}...")

        print(f"Quizs done. Found {len(error_list)} errors")
        return error_list
