import bs4
import requests
import urllib3

from django.core.management import BaseCommand

from api import utilities_notion


# because we set verified=False in requests.get()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL_SUFFIX_IGNORE_LIST = [".pdf"]


class Command(BaseCommand):
    """
    Goal:
    Populate in Notion the new fields we created: answer_accessible_url_text & answer_scientific_url_text  # noqa

    How-to:
    Run the script as many times as needed to update the new or remaining questions that have
    their answer_accessible_url field filled but answer_accessible_url_text empty
    (same goes for answer_scientific_url)

    Usage:
    python manage.py populate_url_text_fields_in_notion
    python manage.py populate_url_text_fields_in_notion --field answer_scientific_url
    """
    def add_arguments(self, parser):
        parser.add_argument(
            "--field",
            type=str,
            default="answer_accessible_url",
            help="answer_accessible_url or answer_scientific_url. Default: answer_accessible_url",
        )

    def handle(self, *args, **options):
        #########################################################
        # Init
        #########################################################
        question_field = options["field"]
        questions_updated = 0

        #########################################################
        # Step 1: fetch questions needing to be updated
        #########################################################
        notion_query_filter = {
            "filter": {
                "and": [
                    {"property": question_field, "text": {"is_not_empty": True}},
                    {"property": f"{question_field}_text", "text": {"is_empty": True}}
                ]
            }
        }
        try:
            notion_questions_response = utilities_notion.get_question_table_pages(sort_direction="ascending", extra_data=notion_query_filter)  # noqa
        except:  # noqa
            self.stdout.write("Erreur accès à l'API Notion")
            return

        self.stdout.write(f"Found {len(notion_questions_response.json()['results'])} questions with {question_field}_text missing")  # noqa

        #########################################################
        # Step 2: loop on each question
        # a) fetch the url's title
        # b) update the question page
        #########################################################
        for question in notion_questions_response.json()["results"]:
            self.stdout.write("-" * 80)
            self.stdout.write(f"{question['properties']['id']['number']} / {question['id']}")
            self.stdout.write(f"{question['properties'][question_field]['url']}")

            question_field_url = question["properties"][question_field]["url"]
            question_field_url_text = ""

            if question_field_url and not question_field_url.endswith(".pdf"):
                try:
                    question_field_url_response = requests.get(question_field_url, verify=False)
                    if question_field_url_response.status_code == 200:
                        html = bs4.BeautifulSoup(question_field_url_response.text, "html.parser")
                        if html:
                            if html.title:
                                question_field_url_text = html.title.text.strip()
                except OSError:  # urllib3.exceptions.NewConnectionError:
                    self.stdout.write("Erreur DNS")

            if question_field_url_text:
                data = {
                    "properties": {
                        f"{question_field}_text": {
                            "rich_text": [
                                {"text": {"content": question_field_url_text}}
                            ]
                        }
                    }
                }
                try:
                    utilities_notion.update_page_properties(page_id=question["id"], data=data)
                    questions_updated += 1
                except:  # noqa
                    self.stdout.write("Erreur accès à l'API Notion")
                    return

        #########################################################
        # Done! Recap
        #########################################################
        self.stdout.write("-" * 80)
        self.stdout.write(f"Finished populating field {question_field}")
        self.stdout.write(f"Found {len(notion_questions_response.json()['results'])} questions")
        self.stdout.write(f"Updated {questions_updated} questions")
