import re

from django.core.management import BaseCommand

from core.models import Configuration
from api import utilities_notion


configuration = Configuration.get_solo()
IMAGE_RAW_PREFIX = "https://raw.githubusercontent.com/raphodn/know-your-planet/master"


class Command(BaseCommand):
    """
    Goal:
    Fix URLs that are hosted on github.com but with the wrong answer_image_url
    - before: https://github.com/raphodn/know-your-planet/blob/master/data/images/questions/13.png?raw=true
    - after: https://raw.githubusercontent.com/raphodn/know-your-planet/master/data/images/questions/13.png

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
                "and": [{
                    "property": "answer_image_url",
                    "text": {
                        "contains": f"{configuration.application_open_source_code_url}/blob/master/data/images/"
                    }
                }],
            }
        }
        try:
            notion_questions_response = utilities_notion.get_question_table_pages(sort_direction="ascending", extra_data=notion_query_filter)  # noqa
        except:  # noqa
            self.stdout.write("Erreur accès à l'API Notion")
            return

        self.stdout.write(f"Found {len(notion_questions_response.json()['results'])} questions with answer_image_url to fix")  # noqa

        #########################################################
        # Step 2: loop on each question
        # a) fetch the url's title
        # b) update the question page
        #########################################################
        for question in notion_questions_response.json()["results"]:
            self.stdout.write("-" * 80)
            self.stdout.write(f"{question['properties']['id']['number']} / {question['id']}")

            question_answer_image_url = question['properties']['answer_image_url']["url"]
            self.stdout.write(f"{question_answer_image_url}")

            if question_answer_image_url:
                image_path = re.findall("https:\/\/github.com\/raphodn\/know-your-planet\/blob\/master\/data\/images\/(.+)\?raw=true", question_answer_image_url)
                if not len(image_path):
                    image_path = re.findall("https:\/\/github.com\/raphodn\/know-your-planet\/blob\/master\/data\/images\/(.+)", question_answer_image_url)
                if len(image_path):
                    new_question_answer_image_url = f"https://raw.githubusercontent.com/raphodn/know-your-planet/master/data/images/{image_path[0]}"
                    data = {
                        "properties": {
                            "answer_image_url": {
                                "url": new_question_answer_image_url
                            }
                        }
                    }
                    try:
                        utilities_notion.update_page_properties(page_id=question["id"], data=data)
                        self.stdout.write(f"{new_question_answer_image_url}")
                        questions_updated += 1
                    except:  # noqa
                        self.stdout.write("Erreur accès à l'API Notion")
                        return

        #########################################################
        # Done! Recap
        #########################################################
        self.stdout.write("-" * 80)
        self.stdout.write(f"Finished populating field answer_image_url")
        self.stdout.write(f"Found {len(notion_questions_response.json()['results'])} questions")
        self.stdout.write(f"Updated {questions_updated} questions")
