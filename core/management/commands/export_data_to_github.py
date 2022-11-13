import time
from datetime import datetime

from django.conf import settings
from django.core.management import BaseCommand
from django.utils import timezone

from api.categories.serializers import CategorySerializer
from api.glossary.serializers import GlossaryItemSerializer
from api.questions.serializers import QuestionSerializer
from api.quizs.serializers import QuizQuestionSerializer, QuizRelationshipSerializer, QuizWithQuestionSerializer
from api.tags.serializers import TagSerializer
from api.users.serializers import UserWithCountSerializer
from categories.models import Category
from core.models import Configuration
from core.utils import github, utilities
from glossary.models import GlossaryItem
from questions.models import Question
from quizs.models import Quiz, QuizQuestion, QuizRelationship
from tags.models import Tag
from users.models import User


category_queryset = Category.objects.all()
tag_queryset = Tag.objects.all()
user_queryset = User.objects.all_contributors().has_public_content()
question_queryset = Question.objects.public()
quiz_queryset = Quiz.objects.public()
quiz_questions_queryset = QuizQuestion.objects.public()
quiz_relationships_queryset = QuizRelationship.objects.all()
glossary_item_queryset = GlossaryItem.objects.all()


class Command(BaseCommand):
    """
    Usage:
    python manage.py export_data_to_github
    python manage.py export_data_to_github --force  # export even if there is no data changes
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            default=False,
            action="store_true",
            dest="force",
            help="Export data even if there are no (visible) changes",
        )

    def handle(self, *args, **options):
        configuration = Configuration.get_solo()

        # check that there is data to update
        if options["force"] or any(
            [
                category_queryset.filter(updated__gte=configuration.github_data_last_exported).exists(),
                tag_queryset.filter(updated__gte=configuration.github_data_last_exported).exists(),
                question_queryset.filter(updated__gte=configuration.github_data_last_exported).exists(),
                quiz_queryset.filter(updated__gte=configuration.github_data_last_exported).exists(),
                quiz_questions_queryset.filter(updated__gte=configuration.github_data_last_exported).exists(),
                quiz_relationships_queryset.filter(updated__gte=configuration.github_data_last_exported).exists(),
                glossary_item_queryset.filter(updated__gte=configuration.github_data_last_exported).exists(),
            ]
        ):
            # init
            start_time = time.time()

            current_datetime = datetime.now()
            current_datetime_string = current_datetime.strftime("%Y-%m-%d-%H-%M")
            current_datetime_string_pretty = current_datetime.strftime("%Y-%m-%d %H:%M")
            branch_name = f"update-data-{current_datetime_string}"
            pull_request_name = f"Data: update data ({current_datetime_string_pretty})"

            # update configuration first
            # why? to have the new date in the configuration.yaml
            # issue: if there is an error during the export, 'github_data_last_exported' is still updated
            configuration.github_data_last_exported = timezone.now()
            configuration.save()

            print("--- Step 1 done : init (%s seconds) ---" % round(time.time() - start_time, 1))

            # update & commit data files
            try:
                #####################################
                # data/configuration.yaml
                start_time = time.time()
                configuration_yaml = utilities.serialize_model_to_yaml_old(
                    "core", model_label="configuration", flat=True
                )
                configuration_element = github.create_file_element(
                    file_path="data/configuration.yaml", file_content=configuration_yaml
                )

                print("--- Step 2.1 done : configuration.yaml (%s seconds) ---" % round(time.time() - start_time, 1))

                #####################################
                # # data/categories.yaml
                start_time = time.time()
                categories_yaml = utilities.serialize_model_to_yaml(
                    model_queryset=category_queryset, model_serializer=CategorySerializer
                )  # noqa
                categories_element = github.create_file_element(
                    file_path="data/categories.yaml", file_content=categories_yaml
                )

                print("--- Step 2.2 done : categories.yaml (skipped) ---")

                #####################################
                # data/tags.yaml
                start_time = time.time()
                tags_yaml = utilities.serialize_model_to_yaml(
                    model_queryset=tag_queryset, model_serializer=TagSerializer
                )
                tags_element = github.create_file_element(file_path="data/tags.yaml", file_content=tags_yaml)

                print("--- Step 2.3 done : tags.yaml (%s seconds) ---" % round(time.time() - start_time, 1))

                #####################################
                # data/authors.yaml
                start_time = time.time()
                users_yaml = utilities.serialize_model_to_yaml(
                    model_queryset=user_queryset, model_serializer=UserWithCountSerializer
                )
                users_element = github.create_file_element(file_path="data/authors.yaml", file_content=users_yaml)

                print("--- Step 2.4 done : authors.yaml (%s seconds) ---" % round(time.time() - start_time, 1))

                #####################################
                # data/questions.yaml
                start_time = time.time()
                questions_yaml = utilities.serialize_model_to_yaml(
                    model_queryset=question_queryset, model_serializer=QuestionSerializer
                )
                questions_element = github.create_file_element(
                    file_path="data/questions.yaml", file_content=questions_yaml
                )

                print("--- Step 2.5 done : questions.yaml (%s seconds) ---" % round(time.time() - start_time, 1))

                #####################################
                # data/quizs.yaml
                start_time = time.time()
                quizs_yaml = utilities.serialize_model_to_yaml(
                    model_queryset=quiz_queryset, model_serializer=QuizWithQuestionSerializer
                )
                quizs_element = github.create_file_element(file_path="data/quizs.yaml", file_content=quizs_yaml)

                print("--- Step 2.6 done : quizs.yaml (%s seconds) ---" % round(time.time() - start_time, 1))

                #####################################
                # data/quiz-questions.yaml
                start_time = time.time()
                quiz_questions_yaml = utilities.serialize_model_to_yaml(
                    model_queryset=quiz_questions_queryset, model_serializer=QuizQuestionSerializer
                )
                quiz_questions_element = github.create_file_element(
                    file_path="data/quiz-questions.yaml", file_content=quiz_questions_yaml
                )

                print("--- Step 2.7 done : quiz-questions.yaml (%s seconds) ---" % round(time.time() - start_time, 1))

                #####################################
                # data/quiz-relationships.yaml
                start_time = time.time()
                quiz_relationships_yaml = utilities.serialize_model_to_yaml(
                    model_queryset=quiz_relationships_queryset, model_serializer=QuizRelationshipSerializer
                )
                quiz_relationships_element = github.create_file_element(
                    file_path="data/quiz-relationships.yaml",
                    file_content=quiz_relationships_yaml,
                )

                print(
                    "--- Step 2.8 done : quiz-relationships.yaml (%s seconds) ---" % round(time.time() - start_time, 1)
                )

                #####################################
                # data/ressources-glossaire.yaml
                start_time = time.time()
                glossary_items_yaml = utilities.serialize_model_to_yaml(
                    model_queryset=glossary_item_queryset, model_serializer=GlossaryItemSerializer
                )
                glossary_items_element = github.create_file_element(
                    file_path="data/ressources-glossaire.yaml",
                    file_content=glossary_items_yaml,
                )

                print(
                    "--- Step 2.9 done : ressources-glossaire.yaml (%s seconds) ---"
                    % round(time.time() - start_time, 1)
                )

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

                print("--- Step 2.10 done : constants.js (%s seconds) ---" % round(time.time() - start_time, 1))

                #####################################
                # commit files
                start_time = time.time()

                github.update_multiple_files(
                    branch_name=branch_name,
                    commit_message="Data: data update",
                    file_element_list=[
                        configuration_element,
                        categories_element,
                        tags_element,
                        users_element,
                        questions_element,
                        quizs_element,
                        quiz_questions_element,
                        quiz_relationships_element,
                        glossary_items_element,
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
                        "Mise à jour de la donnée :"
                        "<ul>"
                        "<li>data/configuration.yaml</li>"
                        "<li>data/tags.yaml</li>"
                        "<li>data/contributors.yaml</li>"
                        "<li>data/questions.yaml</li>"
                        "<li>data/quizs.yaml</li>"
                        "<li>data/quiz-questions.yaml</li>"
                        "<li>data/quiz-relationships.yaml</li>"
                        "<li>data/ressources-glossaire.yaml</li>"
                        "</ul>"
                    )
                    pull_request = github.create_pull_request(
                        pull_request_title=pull_request_name,
                        pull_request_message=pull_request_message,
                        branch_name=branch_name,
                        pull_request_labels="automerge",
                    )

                    print(
                        "--- Step 4 done : created Pull Request (%s seconds) ---" % round(time.time() - start_time, 1)
                    )

                    # return
                    self.stdout.write(pull_request.html_url)
            except Exception as e:
                print(e)
                self.stdout.write(str(e))
        else:
            self.stdout.write("No data to update since last export")
