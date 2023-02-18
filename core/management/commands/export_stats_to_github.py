import time
from datetime import datetime

import yaml
from django.conf import settings
from django.core.management import BaseCommand
from django.utils import timezone, translation

from core.models import Configuration
from core.utils import github, utilities
from stats import utilities as utilities_stats


class Command(BaseCommand):
    """
    Usage:
    python manage.py export_stats_to_github
    """

    def handle(self, *args, **options):
        translation.activate("en")

        # init
        start_time = time.time()

        current_datetime = datetime.now()
        current_datetime_string = current_datetime.strftime("%Y-%m-%d-%H-%M")
        current_datetime_string_pretty = current_datetime.strftime("%Y-%m-%d %H:%M")
        branch_name = f"update-stats-{current_datetime_string}"
        pull_request_name = f"Data: update stats ({current_datetime_string_pretty})"

        # update configuration first
        configuration = Configuration.get_solo()
        configuration.github_stats_last_exported = timezone.now()
        configuration.save()

        print("--- Step 1 done : init (%s seconds) ---" % round(time.time() - start_time, 1))

        # update & commit stats files
        try:
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
            stats_element = github.create_file_element(file_path="data/stats.yaml", file_content=stats_yaml)

            print("--- Step 2.1 done : stats.yaml (%s seconds) ---" % round(time.time() - start_time, 1))

            #####################################
            # data/difficulty-levels.yaml
            start_time = time.time()
            difficulty_levels_list = utilities_stats.difficulty_aggregate()
            difficulty_levels_yaml = yaml.safe_dump(difficulty_levels_list, allow_unicode=True, sort_keys=False)
            difficulty_levels_element = github.create_file_element(
                file_path="data/difficulty-levels.yaml",
                file_content=difficulty_levels_yaml,
            )

            print("--- Step 2.2 done : difficulty-levels.yaml (%s seconds) ---" % round(time.time() - start_time, 1))

            # #####################################
            # # data/authors.yaml
            # start_time = time.time()
            # authors_list = utilities_stats.author_aggregate()
            # authors_yaml = yaml.safe_dump(authors_list, allow_unicode=True, sort_keys=False)
            # authors_element = github.create_file_element(file_path="data/authors.yaml", file_content=authors_yaml)

            # print("--- Step 2.3 done : authors.yaml (%s seconds) ---" % round(time.time() - start_time, 1))

            #####################################
            # data/languages.yaml
            start_time = time.time()
            languages_list = utilities_stats.language_aggregate()
            languages_yaml = yaml.safe_dump(languages_list, allow_unicode=True, sort_keys=False)
            languages_element = github.create_file_element(
                file_path="data/languages.yaml", file_content=languages_yaml
            )

            print("--- Step 2.4 done : languages.yaml (%s seconds) ---" % round(time.time() - start_time, 1))

            # #####################################
            # # data/quiz-stats.yaml
            # start_time = time.time()
            # quiz_detail_stats_list = utilities_stats.quiz_detail_stats()
            # quiz_detail_stats_yaml = yaml.safe_dump(quiz_detail_stats_list, allow_unicode=True, sort_keys=False)
            # quiz_stats_element = github.create_file_element(
            #     file_path="data/quiz-stats.yaml", file_content=quiz_detail_stats_yaml
            # )

            # print("--- Step 2.5 done : quiz-stats.yaml (%s seconds) ---" % round(time.time() - start_time, 1))

            #####################################
            # update frontend file with timestamp
            # frontend/src/constants.js
            start_time = time.time()
            old_frontend_constants_file_content = github.get_file(
                file_path="frontend/src/constants.js",
            )
            new_frontend_constants_file_content_string = utilities.update_frontend_last_updated_datetime(  # noqa
                old_frontend_constants_file_content.decoded_content.decode(),
                current_datetime_string_pretty,
            )
            new_frontend_constants_file_element = github.create_file_element(
                file_path="frontend/src/constants.js",
                file_content=new_frontend_constants_file_content_string,
            )

            print("--- Step 2.6 done : constants.js (%s seconds) ---" % round(time.time() - start_time, 1))

            #####################################
            # commit files
            start_time = time.time()

            github.update_multiple_files(
                branch_name=branch_name,
                commit_message="Data: stats update",
                file_element_list=[
                    stats_element,
                    difficulty_levels_element,
                    # authors_element,
                    languages_element,
                    # quiz_stats_element,
                    new_frontend_constants_file_element,
                ],
            )

            print("--- Step 3 done : committed to branch (%s seconds) ---" % round(time.time() - start_time, 1))

            #####################################
            # create pull request
            start_time = time.time()

            if not settings.DEBUG:
                # create pull request
                pull_request_message = (
                    "Mise à jour des stats :"
                    "<ul>"
                    "<li>data/stats.yaml</li>"
                    "<li>data/difficulty-levels.yaml</li>"
                    # "<li>data/authors.yaml</li>"
                    "<li>data/languages.yaml</li>"
                    "<li>data/tags.yaml</li>"
                    # "<li>data/quiz-stats.yaml</li>"
                    "</ul>"
                )
                pull_request = github.create_pull_request(
                    pull_request_title=pull_request_name,
                    pull_request_message=pull_request_message,
                    branch_name=branch_name,
                    pull_request_labels="automerge",
                )

                print("--- Step 4 done : created Pull Request (%s seconds) ---" % round(time.time() - start_time, 1))

                # return
                self.stdout.write(pull_request.html_url)
        except Exception as e:
            print(e)
            self.stdout.write(str(e))
