# flake8: noqa W605
import re

from django.core.management import BaseCommand

from core.models import Configuration
from core.utils import notion


configuration = Configuration.get_solo()
IMAGE_RAW_PREFIX = "https://raw.githubusercontent.com/quiz-anthropocene/know-your-planet/master"


class Command(BaseCommand):
    """
    Goal:
    Fix URLs that are hosted on github.com but with the wrong answer_image_url
    - before: https://github.com/quiz-anthropocene/know-your-planet/blob/master/data/images/questions/13.png?raw=true  # noqa
    - after: https://raw.githubusercontent.com/quiz-anthropocene/know-your-planet/master/data/images/questions/13.png  # noqa

    How-to:
    Run the script as many times as needed to update the questions that are concerned

    Usage:
    python manage.py fix_answer_image_urls_in_notion
    """

    def handle(self, *args, **options):
        #########################################################
        # Init
        #########################################################
        questions_updated = 0

        #########################################################
        # Step 1: fetch questions needing to be updated
        #########################################################
        notion_query_filter = {
            "filter": {
                "and": [
                    {
                        "property": "answer_image_url",
                        "text": {
                            "contains": f"{configuration.application_open_source_code_url}/blob/master/data/images/"  # noqa
                        },
                    }
                ],
            }
        }
        try:
            notion_questions_response = notion.get_question_table_pages(
                sort_direction="ascending", extra_data=notion_query_filter
            )  # noqa
        except:  # noqa
            self.stdout.write("Erreur accès à l'API Notion")
            return

        self.stdout.write(
            f"Found {len(notion_questions_response.json()['results'])} questions with answer_image_url to fix"
        )  # noqa

        #########################################################
        # Step 2: loop on each question
        # a) fetch the url's title
        # b) update the question page
        #########################################################
        for question in notion_questions_response.json()["results"]:
            self.stdout.write("-" * 80)
            self.stdout.write(f"{question['properties']['id']['number']} / {question['id']}")

            question_answer_image_url = question["properties"]["answer_image_url"]["url"]
            self.stdout.write(f"{question_answer_image_url}")

            if question_answer_image_url:
                image_path = re.findall(
                    "https:\/\/github.com\/raphodn\/know-your-planet\/blob\/master\/data\/images\/(.+)\?raw=true",
                    question_answer_image_url,
                )  # noqa
                if not len(image_path):
                    image_path = re.findall(
                        "https:\/\/github.com\/raphodn\/know-your-planet\/blob\/master\/data\/images\/(.+)",
                        question_answer_image_url,
                    )  # noqa
                if len(image_path):
                    new_question_answer_image_url = f"{IMAGE_RAW_PREFIX}/data/images/{image_path[0]}"  # noqa
                    data = {"properties": {"answer_image_url": {"url": new_question_answer_image_url}}}
                    try:
                        notion.update_page_properties(page_id=question["id"], data=data)
                        self.stdout.write(f"{new_question_answer_image_url}")
                        questions_updated += 1
                    except:  # noqa
                        self.stdout.write("Erreur accès à l'API Notion")
                        return

        #########################################################
        # Done! Recap
        #########################################################
        self.stdout.write("-" * 80)
        self.stdout.write("Finished populating field answer_image_url")
        self.stdout.write(f"Found {len(notion_questions_response.json()['results'])} questions")
        self.stdout.write(f"Updated {questions_updated} questions")
