import time
import yaml
from datetime import datetime

from django.utils import timezone
from django.conf import settings
from django.core.management import BaseCommand

from api import utilities, utilities_github
from stats import utilities as utilities_stats
from api.models import Configuration


class Command(BaseCommand):
    """
    Usage:
    python manage.py export_data_to_github

    TODO:
    - commit multiple files at once ? https://github.com/PyGithub/PyGithub/issues/1628
    """

    def handle(self, *args, **options):
        # init
        start_time = time.time()

        current_datetime = datetime.now()
        current_datetime_string = current_datetime.strftime("%Y-%m-%d-%H-%M")
        current_datetime_string_pretty = current_datetime.strftime("%Y-%m-%d %H:%M")
        data_update_branch_name = f"data-update-{current_datetime_string}"
        data_update_pull_request_name = (
            f"Data: update ({current_datetime_string_pretty})"
        )

        # update configuration first
        configuration = Configuration.get_solo()
        configuration.github_last_exported = timezone.now()
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
            # data/stats.yaml
            start_time = time.time()
            stats_dict = {
                **utilities_stats.question_stats(),
                **utilities_stats.quiz_stats(),
                **utilities_stats.answer_stats(),
                **utilities_stats.category_stats(),
                **utilities_stats.tag_stats(),
                **utilities_stats.contribution_stats(),
            }
            stats_yaml = yaml.safe_dump(stats_dict, allow_unicode=True, sort_keys=False)
            stats_element = utilities_github.create_file_element(
                file_path="data/stats.yaml", file_content=stats_yaml
            )

            print(
                "--- Step 2.2 done : stats.yaml (%s seconds) ---"
                % round(time.time() - start_time, 1)
            )

            #####################################
            # data/difficulty-levels.yaml
            start_time = time.time()
            difficulty_levels_list = utilities_stats.difficulty_aggregate()
            difficulty_levels_yaml = yaml.safe_dump(
                difficulty_levels_list, allow_unicode=True, sort_keys=False
            )
            difficulty_levels_element = utilities_github.create_file_element(
                file_path="data/difficulty-levels.yaml",
                file_content=difficulty_levels_yaml,
            )

            print(
                "--- Step 2.3 done : difficulty-levels.yaml (%s seconds) ---"
                % round(time.time() - start_time, 1)
            )

            #####################################
            # data/authors.yaml
            start_time = time.time()
            authors_list = utilities_stats.author_aggregate()
            authors_yaml = yaml.safe_dump(
                authors_list, allow_unicode=True, sort_keys=False
            )
            authors_element = utilities_github.create_file_element(
                file_path="data/authors.yaml", file_content=authors_yaml
            )

            print(
                "--- Step 2.4 done : authors.yaml (%s seconds) ---"
                % round(time.time() - start_time, 1)
            )

            #####################################
            # data/languages.yaml
            start_time = time.time()
            languages_list = utilities_stats.language_aggregate()
            languages_yaml = yaml.safe_dump(
                languages_list, allow_unicode=True, sort_keys=False
            )
            languages_element = utilities_github.create_file_element(
                file_path="data/languages.yaml", file_content=languages_yaml
            )

            print(
                "--- Step 2.5 done : languages.yaml (%s seconds) ---"
                % round(time.time() - start_time, 1)
            )

            #####################################
            # # data/categories.yaml
            # start_time = time.time()
            # categories_yaml = utilities.serialize_model_to_yaml(model_label="category", flat=True)
            # categories_element = utilities_github.create_file_element(
            #     file_path="data/categories.yaml",
            #     file_content=categories_element
            # )

            # print(
            #     "--- Step 2.5 done : categories.yaml (%s seconds) ---"
            #     % round(time.time() - start_time, 1)
            # )

            #####################################
            # data/tags.yaml
            start_time = time.time()
            tags_yaml = utilities.serialize_model_to_yaml(model_label="tag", flat=True)
            tags_element = utilities_github.create_file_element(
                file_path="data/tags.yaml", file_content=tags_yaml
            )

            print(
                "--- Step 2.6 done : tags.yaml (%s seconds) ---"
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
                "--- Step 2.7 done : questions.yaml (%s seconds) ---"
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
                "--- Step 2.8 done : quizzes.yaml (%s seconds) ---"
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
                "--- Step 2.9 done : quiz-questions.yaml (%s seconds) ---"
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
                "--- Step 2.10 done : quiz-relationships.yaml (%s seconds) ---"
                % round(time.time() - start_time, 1)
            )

            #####################################
            # data/quiz-stats.yaml
            start_time = time.time()
            quiz_detail_stats_list = utilities_stats.quiz_detail_stats()
            quiz_detail_stats_yaml = yaml.safe_dump(
                quiz_detail_stats_list, allow_unicode=True, sort_keys=False
            )
            quiz_stats_element = utilities_github.create_file_element(
                file_path="data/quiz-stats.yaml", file_content=quiz_detail_stats_yaml
            )

            print(
                "--- Step 2.11 done : quiz-stats.yaml (%s seconds) ---"
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
                "--- Step 2.12 done : constants.js (%s seconds) ---"
                % round(time.time() - start_time, 1)
            )

            #####################################
            # commit files
            start_time = time.time()

            utilities_github.update_multiple_files(
                branch_name=data_update_branch_name,
                commit_message="Data: daily update",
                file_element_list=[
                    configuration_element,
                    stats_element,
                    difficulty_levels_element,
                    authors_element,
                    languages_element,
                    tags_element,
                    questions_element,
                    quizzes_element,
                    quiz_questions_element,
                    quiz_relationships_element,
                    quiz_stats_element,
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
                    "<li>data/stats.yaml</li>"
                    "<li>data/difficulty-levels.yaml</li>"
                    "<li>data/authors.yaml</li>"
                    "<li>data/languages.yaml</li>"
                    "<li>data/tags.yaml</li>"
                    "<li>data/questions.yaml</li>"
                    "<li>data/quizzes.yaml</li>"
                    "<li>data/quiz-questions.yaml</li>"
                    "<li>data/quiz-relationships.yaml</li>"
                    "<li>data/quiz-stats.yaml</li>"
                    "</ul>"
                )
                pull_request = utilities_github.create_pull_request(
                    pull_request_title=data_update_pull_request_name,
                    pull_request_message=pull_request_message,
                    branch_name=data_update_branch_name,
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
