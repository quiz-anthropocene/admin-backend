import time
from datetime import datetime

from django.utils import timezone
from django.conf import settings
from django.core.management import BaseCommand

from core.models import Configuration
from api import utilities, utilities_github


class Command(BaseCommand):
    """
    Usage:
    python manage.py export_data_to_github
    """

    def handle(self, *args, **options):
        # init
        start_time = time.time()

        current_datetime = datetime.now()
        current_datetime_string = current_datetime.strftime("%Y-%m-%d-%H-%M")
        current_datetime_string_pretty = current_datetime.strftime("%Y-%m-%d %H:%M")
        branch_name = f"update-data-{current_datetime_string}"
        pull_request_name = f"Update: data ({current_datetime_string_pretty})"

        # update configuration first
        configuration = Configuration.get_solo()
        configuration.github_data_last_exported = timezone.now()
        configuration.save()

        print(
            "--- Step 1 done : init (%s seconds) ---"
            % round(time.time() - start_time, 1)
        )

        # update & commit data files
        try:
            #####################################
            # data/configuration.yaml
            start_time = time.time()
            configuration_yaml = utilities.serialize_model_to_yaml(
                model_label="configuration", flat=True
            )
            configuration_element = utilities_github.create_file_element(
                file_path="data/configuration.yaml", file_content=configuration_yaml
            )

            print(
                "--- Step 2.1 done : configuration.yaml (%s seconds) ---"
                % round(time.time() - start_time, 1)
            )

            #####################################
            # # data/categories.yaml
            start_time = time.time()
            # categories_yaml = utilities.serialize_model_to_yaml(model_label="category", flat=True)
            # categories_element = utilities_github.create_file_element(
            #     file_path="data/categories.yaml",
            #     file_content=categories_element
            # )

            print("--- Step 2.2 done : categories.yaml (skipped) ---")

            #####################################
            # data/tags.yaml
            start_time = time.time()
            tags_yaml = utilities.serialize_model_to_yaml(model_label="tag", flat=True)
            tags_element = utilities_github.create_file_element(
                file_path="data/tags.yaml", file_content=tags_yaml
            )

            print(
                "--- Step 2.3 done : tags.yaml (%s seconds) ---"
                % round(time.time() - start_time, 1)
            )

            #####################################
            # data/questions.yaml
            start_time = time.time()
            questions_yaml = utilities.serialize_model_to_yaml(
                model_label="question", flat=True
            )
            questions_element = utilities_github.create_file_element(
                file_path="data/questions.yaml", file_content=questions_yaml
            )

            print(
                "--- Step 2.4 done : questions.yaml (%s seconds) ---"
                % round(time.time() - start_time, 1)
            )

            #####################################
            # data/quizzes.yaml
            start_time = time.time()
            quizzes_yaml = utilities.serialize_model_to_yaml(
                model_label="quiz", flat=True
            )
            quizzes_element = utilities_github.create_file_element(
                file_path="data/quizzes.yaml", file_content=quizzes_yaml
            )

            print(
                "--- Step 2.5 done : quizzes.yaml (%s seconds) ---"
                % round(time.time() - start_time, 1)
            )

            #####################################
            # data/quiz-questions.yaml
            start_time = time.time()
            quiz_questions_yaml = utilities.serialize_model_to_yaml(
                model_label="quizquestion", flat=True
            )
            quiz_questions_element = utilities_github.create_file_element(
                file_path="data/quiz-questions.yaml", file_content=quiz_questions_yaml
            )

            print(
                "--- Step 2.6 done : quiz-questions.yaml (%s seconds) ---"
                % round(time.time() - start_time, 1)
            )

            #####################################
            # data/quiz-relationships.yaml
            start_time = time.time()
            quiz_relationships_yaml = utilities.serialize_model_to_yaml(
                model_label="quizrelationship", flat=True
            )
            quiz_relationships_element = utilities_github.create_file_element(
                file_path="data/quiz-relationships.yaml",
                file_content=quiz_relationships_yaml,
            )

            print(
                "--- Step 2.7 done : quiz-relationships.yaml (%s seconds) ---"
                % round(time.time() - start_time, 1)
            )

            #####################################
            # update frontend file with timestamp
            # frontend/src/constants.js
            start_time = time.time()
            old_frontend_constants_file_content = utilities_github.get_file(
                file_path="frontend/src/constants.js",
            )
            new_frontend_constants_file_content_string = utilities.update_frontend_last_updated_datetime(  # noqa
                old_frontend_constants_file_content.decoded_content.decode(),
                current_datetime_string_pretty,
            )
            new_frontend_constants_file_element = utilities_github.create_file_element(
                file_path="frontend/src/constants.js",
                file_content=new_frontend_constants_file_content_string,
            )

            print(
                "--- Step 2.8 done : constants.js (%s seconds) ---"
                % round(time.time() - start_time, 1)
            )

            #####################################
            # commit files
            start_time = time.time()

            utilities_github.update_multiple_files(
                branch_name=branch_name,
                commit_message="Data: data update",
                file_element_list=[
                    configuration_element,
                    tags_element,
                    questions_element,
                    quizzes_element,
                    quiz_questions_element,
                    quiz_relationships_element,
                    new_frontend_constants_file_element,
                ],
            )

            print(
                "--- Step 3 done : committed to branch (%s seconds) ---"
                % round(time.time() - start_time, 1)
            )

            #####################################
            # create pull request
            start_time = time.time()

            if not settings.DEBUG:
                # create pull request
                pull_request_message = (
                    "Mise à jour de la donnée :"
                    "<ul>"
                    "<li>data/configuration.yaml</li>"
                    "<li>data/tags.yaml</li>"
                    "<li>data/questions.yaml</li>"
                    "<li>data/quizzes.yaml</li>"
                    "<li>data/quiz-questions.yaml</li>"
                    "<li>data/quiz-relationships.yaml</li>"
                    "</ul>"
                )
                pull_request = utilities_github.create_pull_request(
                    pull_request_title=pull_request_name,
                    pull_request_message=pull_request_message,
                    branch_name=branch_name,
                    pull_request_labels="automerge",
                )

                print(
                    "--- Step 4 done : created Pull Request (%s seconds) ---"
                    % round(time.time() - start_time, 1)
                )

                # return
                self.stdout.write(pull_request.html_url)
        except Exception as e:
            print(e)
            self.stdout.write(str(e))
