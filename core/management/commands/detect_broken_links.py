import requests
from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand

from questions.models import Question
from quizs.models import Quiz


COMMAND_TITLE = "Commande de détection des liens cassés"


QUESTION_URL_FIELDS = Question.QUESTION_URL_FIELDS + Question.QUESTION_IMAGE_URL_FIELDS
QUIZ_URL_FIELDS = Quiz.QUIZ_URL_FIELDS + Quiz.QUIZ_IMAGE_URL_FIELDS
# GLOSSARY_ITEM_URL_FIELDS = GlossaryItem.GLOSSARY_ITEM_URL_FIELDS
# USER_CARD_URL_FIELDS =


class Command(BaseCommand):
    """
    Usage:
    python manage.py detect_broken_links
    """

    def handle(self, *args, **options):
        print("=== detect_broken_links running")

        error_list = list()

        question_error_list = self.detect_question_broken_links()
        error_list.extend(question_error_list)
        quiz_error_list = self.detect_quiz_broken_links()
        error_list.extend(quiz_error_list)

        # only send recap email if there are errors
        if len(error_list):
            self.send_recap_email(error_list)

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
                                "object_validation_status": object.validation_status,
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
                                "object_validation_status": object.validation_status,
                                "object_field_name": object_url_field,
                                "object_field_url": url,
                            }
                        )
            progress += 1
            if (progress % 10) == 0:
                print(f"{progress}...")

        print(f"Quizs done. Found {len(error_list)} errors")
        return error_list

    def send_recap_email(self, error_list):
        email_subject = f"[Admin] {COMMAND_TITLE}"

        email_template_html = f"<!DOCTYPE html><html><h1>{COMMAND_TITLE}</h1>"
        email_template_html += f"<p>{len(error_list)} liens cassés</p>"
        email_template_html += "<table border=1><thead><tr><th>Type</th><th>ID</th><th>Statut</th><th>Nom du champ</th><th>Lien cassé</th></tr></thead><tbody>"  # noqa
        for error in error_list:
            email_template_html += f"<tr><td>{error['object_type']}</td><td>{error['object_id']}</td><td>{error['object_validation_status']}</td><td>{error['object_field_name']}</td><td>{error['object_field_url']}</td></tr>"  # noqa
        email_template_html += "</tbody></table></html>"

        send_mail(
            subject=email_subject,
            message=email_template_html,
            html_message=email_template_html,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
            fail_silently=False,
        )
        print("E-mail recap envoyé")
