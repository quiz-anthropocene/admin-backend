import collections
import time
from datetime import datetime, timedelta

import notion
from django.core.exceptions import ValidationError
from django.core.management import BaseCommand
from django.db import IntegrityError
from django.db.models.fields import URLField
from django.utils import timezone

from categories.models import Category
from contributions.models import Contribution
from core import constants
from core.models import Configuration
from core.utils import notion as utilities_notion, utilities
from questions.models import Question
from quizs.models import Quiz
from tags.models import Tag


SKIP_QUESTIONS_LAST_UPDATED_SINCE_DAYS = 15
QUESTION_URL_FIELDS = [field.name for field in Question._meta.fields if type(field) == URLField]


class Command(BaseCommand):
    """
    Usage:
    - python manage.py import_questions_from_notion 0  # all
    - python manage.py import_questions_from_notion 1
    - python manage.py import_questions_from_notion 0 --skip-old

    Help:
    - '///' ? delimeter to show lists (string split) in the template
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "scope",
            type=int,
            choices=constants.NOTION_QUESTIONS_IMPORT_SCOPE_LIST,
            help="0 = all, 1 = first X, 2 = second X",
        )
        parser.add_argument(
            "--skip-old",
            default=False,
            action="store_true",
            dest="skip-old",
            help="Skip processing of old questions (last updated > 15 days)",
        )

    def handle(self, *args, **options):
        #########################################################
        # Init
        #########################################################
        scope = options["scope"]

        notion_questions_list = []
        questions_ids_duplicate = []
        questions_ids_missing = []
        tags_created = []
        questions_created = []
        questions_updated = set()
        questions_updates = {}
        validation_errors = []

        all_categories_list = list(Category.objects.all())
        all_tags_name_list = list(Tag.objects.all().values_list("name", flat=True))

        #########################################################
        # Fetch questions from Notion
        #########################################################
        start_time = time.time()

        try:
            notion_questions_list = utilities_notion.get_questions_table_rows()
        except:  # noqa
            self.stdout.write("Erreur accès Notion. token_v2 expiré ?")
            return

        self.stdout.write(
            "--- Step 1 done : fetch questions from Notion (%s seconds) ---" % round(time.time() - start_time, 1)
        )

        #########################################################
        # Check question ids (duplicates & missing)
        #########################################################
        start_time = time.time()

        # order by notion_questions_list by id
        notion_questions_list = sorted(notion_questions_list, key=lambda question: question.get_property("id") or 0)
        # check if id duplicates
        notion_questions_id_list = [
            question.get_property("id") for question in notion_questions_list if question.get_property("id")
        ]
        questions_ids_duplicate = [
            item for item, count in collections.Counter(notion_questions_id_list).items() if count > 1
        ]
        # check if id 'missing'
        for n in range(1, notion_questions_id_list[-1]):
            if n not in notion_questions_id_list:
                questions_ids_missing.append(n)

        self.stdout.write(
            "--- Step 2 done : check question ids (duplicates & missing) : %s seconds ---"
            % round(time.time() - start_time, 1)
        )

        #########################################################
        # Loop on questions and create, update, store validation_errors
        #########################################################
        start_time = time.time()

        # reduce scope because of timeouts on Heroku (30 seconds)
        if scope:
            min_question_id = 200 * (scope - 1)
            max_question_id = 200 * scope
            notion_questions_list_scope = notion_questions_list[min_question_id:max_question_id]
        else:
            notion_questions_list_scope = notion_questions_list

        self.stdout.write(f"processing {len(notion_questions_list_scope)} questions")
        self.stdout.write(f"First question id : {notion_questions_list_scope[0].get_property('id')}")
        self.stdout.write(f"Last question id : {notion_questions_list_scope[-1].get_property('id')}")

        for notion_question_row in notion_questions_list_scope:
            question_validation_errors = []
            notion_question_tag_objects = []
            notion_question_last_updated = notion_question_row.get_property("Last edited time").date()  # noqa

            # check question has id
            if notion_question_row.get_property("id") is None:
                question_validation_errors.append(ValidationError({"id": "Question sans id. vide ?"}))
            # ignore questions not updated recently
            elif options.get("skip-old") and (
                notion_question_last_updated
                < (datetime.now().date() - timedelta(days=SKIP_QUESTIONS_LAST_UPDATED_SINCE_DAYS))
            ):
                pass
            else:
                # build question_dict from notion_row
                notion_question_dict = self.transform_notion_question_row_to_question_dict(notion_question_row)

                # if notion_question_dict["id"] == 1014:
                #     self.stdout.write(notion_question_dict)

                # cleanup relation category
                # - check category exists
                # error if unknown category : api.models.DoesNotExist: Category matching query does not exist.  # noqa
                if notion_question_dict["category"] is not None:
                    notion_question_category_id = next(
                        (c.id for c in all_categories_list if c.name == notion_question_dict["category"]),
                        None,
                    )
                    if notion_question_category_id:
                        notion_question_dict["category_id"] = notion_question_category_id
                        del notion_question_dict["category"]
                    else:
                        question_validation_errors.append(
                            ValidationError(
                                {
                                    "category": f"Question {notion_question_dict['id']}. "
                                    f"Category '{notion_question_dict['category']}' inconnue"
                                }
                            )
                        )

                # cleanup relation tags
                # - if no tags, notion returns [""]
                # - check tags exist, create them if not
                # - then delete the "tags" key, we will make the M2M join later
                notion_question_tag_name_list = []
                if notion_question_dict["tags"] != [""]:
                    notion_question_tag_name_list = [
                        tag for tag in notion_question_dict["tags"] if not tag.startswith("Quiz")
                    ]
                    new_tags = [
                        new_tag for new_tag in notion_question_tag_name_list if new_tag not in all_tags_name_list
                    ]
                    # create missing tags
                    if len(new_tags):
                        Tag.objects.bulk_create([Tag(name=new_tag) for new_tag in new_tags])
                        all_tags_name_list += new_tags
                        tags_created += new_tags
                del notion_question_dict["tags"]

            # create or update
            # - if the question does not have validation_errors
            if len(question_validation_errors):
                validation_errors += question_validation_errors
            # - if the question has been updated recently
            elif options.get("skip-old") and (
                notion_question_last_updated
                < (datetime.now().date() - timedelta(days=SKIP_QUESTIONS_LAST_UPDATED_SINCE_DAYS))
            ):
                pass
            else:
                # the question doesn't have errors : ready to create/update
                try:
                    db_question, created = Question.objects.get_or_create(
                        id=notion_question_dict["id"], defaults=notion_question_dict
                    )
                    # store info
                    if created:
                        notion_question_tag_objects = Tag.objects.filter(name__in=notion_question_tag_name_list)
                        db_question.tags.set(notion_question_tag_objects)
                        questions_created.append(db_question.id)
                    else:
                        questions_updates_key = f"Question {db_question.id}"

                        # update basic fields
                        question_changes_list = self.update_question(db_question, notion_question_dict)

                        if len(question_changes_list):
                            if questions_updates_key in questions_updates:
                                questions_updates[questions_updates_key] += question_changes_list
                            else:
                                questions_updates[questions_updates_key] = question_changes_list
                            questions_updated.add(db_question.id)

                        # update tags
                        question_tag_changes_string = self.update_question_tags(
                            db_question, notion_question_tag_name_list
                        )

                        if question_tag_changes_string:
                            if questions_updates_key in questions_updates:
                                questions_updates[questions_updates_key].append(question_tag_changes_string)
                            else:
                                questions_updates[questions_updates_key] = [question_tag_changes_string]
                            questions_updated.add(db_question.id)

                except ValidationError as e:
                    validation_errors.append(f"Question {notion_question_dict['id']}: {e}")
                except IntegrityError as e:
                    validation_errors.append(f"Question {notion_question_dict['id']}: {e}")

        self.stdout.write("--- Step 3 done : loop on questions : %s seconds ---" % round(time.time() - start_time, 1))

        #########################################################
        # Build and send stats
        #########################################################
        start_time = time.time()

        # done
        questions_notion_count = f"Nombre de questions dans Notion : {len(notion_questions_list)}"
        questions_scope_count = (
            f"Nombre de questions prises en compte ici : {len(notion_questions_list_scope)}"  # noqa
        )
        questions_scope_count += f" (de id {notion_questions_list_scope[0].get_property('id')} à id {notion_questions_list_scope[-1].get_property('id')})"  # noqa
        questions_ids_duplicate_message = (
            f"ids 'en double' : {', '.join([str(question_id) for question_id in questions_ids_duplicate])}"  # noqa
        )
        questions_ids_missing_message = (
            f"ids 'manquants' : {', '.join([str(question_id) for question_id in questions_ids_missing])}"  # noqa
        )

        tags_created_message = f"Nombre de tags ajoutés : {len(tags_created)}"
        if len(tags_created):
            tags_created_message += "\n" + f"Détails : {', '.join([str(tag_name) for tag_name in tags_created])}"

        questions_created_message = f"Nombre de questions ajoutées : {len(questions_created)}"
        if len(questions_created):
            questions_created_message += (
                "\n" + f"Détails : {', '.join([str(question_id) for question_id in questions_created])}"
            )

        questions_updated_message = f"Nombre de questions modifiées : {len(questions_updated)}"
        if len(questions_updates):
            questions_updated_message += "\n" + "\n".join(
                [key + "///" + "///".join(questions_updates[key]) for key in questions_updates]
            )

        # check if any published quiz have non-validated questions
        published_quizs = Quiz.objects.prefetch_related("questions").published()
        for pq in published_quizs:
            pq_not_validated_questions = pq.questions_not_validated_list
            for question in pq_not_validated_questions:
                validation_errors.append(
                    f"Quiz {pq.id}: Question {question.id} is not validated but quiz is published"
                )

        validation_errors_message = "Erreurs : "
        if len(validation_errors):
            validation_errors_message += (
                f"Erreurs : {len(validation_errors)}" + "\n" + "\n".join([str(error) for error in validation_errors])
            )
            Contribution.objects.create(
                text="Erreur(s) lors de l'import",
                description=validation_errors_message,
                type="erreur application",
            )

        # if not settings.DEBUG and scope == 0:
        #     utilities_notion.add_import_stats_row(
        #         len(notion_questions_list),
        #         len(questions_created),
        #         len(questions_updated),
        #     )

        self.stdout.write(
            "--- Step 4 done : build and send stats : %s seconds ---" % round(time.time() - start_time, 1)
        )

        #########################################################
        # Update configuration
        #########################################################
        configuration = Configuration.get_solo()
        if scope:
            setattr(
                configuration,
                f"notion_questions_scope_{scope}_last_imported",
                timezone.now(),
            )
        else:
            for scope in constants.NOTION_QUESTIONS_IMPORT_SCOPE_LIST[1:]:
                setattr(
                    configuration,
                    f"notion_questions_scope_{scope}_last_imported",
                    timezone.now(),
                )
        configuration.save()

        self.stdout.write(
            "\n".join(
                [
                    ">>> Info sur les questions",
                    questions_notion_count,
                    questions_scope_count,
                    questions_ids_duplicate_message,
                    questions_ids_missing_message,
                    "",
                    ">>> Info sur les tags ajoutés",
                    tags_created_message,
                    "",
                    ">>> Info sur les questions ajoutées",
                    questions_created_message,
                    "",
                    ">>> Info sur les questions modifiées",
                    questions_updated_message,
                    "",
                    ">>> Erreurs lors de l'import",
                    validation_errors_message,
                ]
            )
        )

    def transform_notion_question_row_to_question_dict(self, notion_question_row):
        """
        Transform the Notion question row ("dict") into a question dict
        """
        notion_question_dict = dict()

        # fill dict with notion_question_row
        for question_model_field in Question._meta.get_fields():
            try:
                notion_question_property = notion_question_row.get_property(question_model_field.name)
                # cleanup dates
                if type(notion_question_property) == notion.collection.NotionDate:
                    notion_question_property = notion_question_property.start
                notion_question_dict[question_model_field.name] = notion_question_property
            except:  # noqa
                pass

        # cleanup fields
        # - field type --> "" if None
        # - field difficulty to int
        # - field answer_correct --> "" if None
        # - field added --> created time if None --> to date
        # - field validator --> "" if None
        # - fields answer_explanation, answer_image_explanation & answer_extra_info --> clean markdown [links](links)  # noqa
        # - fields '_url' --> strip spaces at end (or else we get a ValidationError)
        if notion_question_dict["type"] is None:
            notion_question_dict["type"] = ""
        if type(notion_question_dict["difficulty"]) == str:
            if notion_question_dict["difficulty"] == "":
                notion_question_dict["difficulty"] = None
            else:
                notion_question_dict["difficulty"] = int(notion_question_dict["difficulty"])
        if notion_question_dict["language"] is None:
            notion_question_dict["language"] = ""
        if notion_question_dict["answer_correct"] is None:
            notion_question_dict["answer_correct"] = ""
        if ("added" not in notion_question_dict) or (notion_question_dict["added"] is None):
            notion_question_dict["added"] = notion_question_row.get_property("Created time").date()
        if notion_question_dict["validator"] is None:
            notion_question_dict["validator"] = ""
        # clean markdown [links](links)
        for field_name in ["answer_explanation", "answer_image_explanation", "answer_extra_info"]:
            if "http" in notion_question_dict[field_name]:
                notion_question_dict[field_name] = utilities.clean_markdown_links(notion_question_dict[field_name])
        # strip spaces in url fields
        for field_name in QUESTION_URL_FIELDS:
            if field_name in notion_question_dict:
                notion_question_dict[field_name] = notion_question_dict[field_name].strip()

        return notion_question_dict

    def update_question(self, db_question, notion_question_dict):
        """
        Update question and get a list of changes
        """
        question_changes = []
        # check possible changes
        # basic fields
        for question_model_field in Question._meta.get_fields():
            if question_model_field.name in notion_question_dict:
                # consider default values in some fields
                if (
                    (notion_question_dict[question_model_field.name] not in [None, ""])
                    and getattr(db_question, question_model_field.name)
                    != notion_question_dict[question_model_field.name]
                ) or (
                    (notion_question_dict[question_model_field.name] in [None, ""])
                    and getattr(db_question, question_model_field.name) != question_model_field.get_default()
                ):
                    # track changes (before updating field to get previous value)
                    db_question_field_update_message = f"champ '{question_model_field.name}' : {getattr(db_question, question_model_field.name)} >>> {notion_question_dict[question_model_field.name]}"  # noqa
                    question_changes.append(db_question_field_update_message)
                    # update field
                    setattr(
                        db_question,
                        question_model_field.name,
                        notion_question_dict[question_model_field.name],
                    )
                    db_question.save(update_fields=[question_model_field.name])
                    # reset question stats in some cases
                    if question_model_field.name == "answer_correct":
                        db_question.agg_stats.answer_count = 0
                        db_question.agg_stats.answer_success_count = 0
                        db_question.agg_stats.save()

        return question_changes

    def update_question_tags(self, db_question, notion_question_tag_name_list):
        """ """
        question_tag_changes = None
        # compare tags
        has_different_tags = [
            different_tag
            for different_tag in notion_question_tag_name_list
            if different_tag not in list(db_question.tags.values_list("name", flat=True))
        ]
        if len(has_different_tags) or (db_question.tags.count() != len(notion_question_tag_name_list)):
            # track changes
            db_question_tag_update_message = f"champ 'tags' : {list(db_question.tags.values_list('name', flat=True))} >>> {notion_question_tag_name_list}"  # noqa
            question_tag_changes = db_question_tag_update_message
            # update tags
            notion_question_tag_objects = Tag.objects.filter(name__in=notion_question_tag_name_list)
            db_question.tags.set(notion_question_tag_objects)

        return question_tag_changes
