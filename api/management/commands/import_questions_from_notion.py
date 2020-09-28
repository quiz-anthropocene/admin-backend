import time
import notion
import collections

from django.conf import settings
from django.core.management import BaseCommand
from django.core.exceptions import ValidationError

from api import utilities, utilities_notion
from api.models import Question, Category, Tag


class Command(BaseCommand):
    """
    Usage:
    - python manage.py import_questions_from_notion
    - python manage.py import_questions_from_notion 1

    TODO: optimise db queries and avoid Category & Tag calls ?

    Help : ||| ? delimeter to show lists (string split) in the template
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "scope", type=int, help="0 = all, 1 = first X, 2 = second X"
        )

    def handle(self, *args, **options):
        scope = options["scope"]
        notion_questions_list = []
        questions_ids_duplicate = []
        questions_ids_missing = []
        questions_created = []
        questions_updated = set()
        questions_updates = []
        validation_errors = []

        all_tags_list = list(Tag.objects.all().values_list("name", flat=True))

        start_time = time.time()

        try:
            notion_questions_list = utilities_notion.get_questions_table_rows()
        except:  # noqa
            self.stdout.write("Erreur accès Notion. token_v2 expiré ?")
            return

        print("--- fetch questions : %s seconds ---" % (time.time() - start_time))
        start_time = time.time()

        # order by notion_questions_list by id
        notion_questions_list = sorted(
            notion_questions_list, key=lambda question: question.get_property("id") or 0
        )
        # check if id duplicates
        notion_questions_id_list = [
            question.get_property("id")
            for question in notion_questions_list
            if question.get_property("id")
        ]
        questions_ids_duplicate = [
            item
            for item, count in collections.Counter(notion_questions_id_list).items()
            if count > 1
        ]
        # check if id 'missing'
        for n in range(1, notion_questions_id_list[-1]):
            if n not in notion_questions_id_list:
                questions_ids_missing.append(n)

        print("--- question ids : %s seconds ---" % (time.time() - start_time))
        start_time = time.time()

        # reduce scope because of timeouts on Heroku (30 seconds)
        if scope == 1:
            notion_questions_list_scope = notion_questions_list[:200]
        elif scope == 2:
            notion_questions_list_scope = notion_questions_list[200:400]
        elif scope == 3:
            notion_questions_list_scope = notion_questions_list[400:]
        else:
            notion_questions_list_scope = notion_questions_list

        for notion_question_row in notion_questions_list_scope:
            notion_question_dict = dict()
            notion_question_tag_objects = []
            question_validation_errors = []

            # fill dict with notion_question_row
            for question_model_field in Question._meta.get_fields():
                try:
                    notion_question_property = notion_question_row.get_property(
                        question_model_field.name
                    )
                    # cleanup dates
                    if type(notion_question_property) == notion.collection.NotionDate:
                        notion_question_property = notion_question_property.start
                    notion_question_dict[
                        question_model_field.name
                    ] = notion_question_property
                except:  # noqa
                    pass

            # cleanup fields
            # - check id exists
            # - field type --> "" if None
            # - field difficulty to int
            # - field added --> created time if None --> to date
            # - field validator --> "" if None
            # - fields answer_explanation & answer_extra_info --> clean markdown [links](links)
            if notion_question_dict["id"] is None:
                question_validation_errors.append(
                    ValidationError({"id": "Question sans id. vide ?"})
                )
            else:
                print(notion_question_dict["id"], notion_question_dict["type"])
            if notion_question_dict["type"] is None:
                notion_question_dict["type"] = ""
            if type(notion_question_dict["difficulty"]) == str:
                notion_question_dict["difficulty"] = int(
                    notion_question_dict["difficulty"]
                )
            if ("added" not in notion_question_dict) or (
                notion_question_dict["added"] is None
            ):
                notion_question_dict["added"] = notion_question_row.get_property(
                    "Created time"
                ).date()
            if notion_question_dict["validator"] is None:
                notion_question_dict["validator"] = ""
            if "http" in notion_question_dict["answer_explanation"]:
                notion_question_dict[
                    "answer_explanation"
                ] = utilities.clean_markdown_links(
                    notion_question_dict["answer_explanation"]
                )
            if "http" in notion_question_dict["answer_extra_info"]:
                notion_question_dict[
                    "answer_extra_info"
                ] = utilities.clean_markdown_links(
                    notion_question_dict["answer_extra_info"]
                )

            # cleanup relation category
            # - check category exists
            # error if unknown category : api.models.DoesNotExist: Category matching query does not exist.  # noqa
            if notion_question_dict["category"] is not None:
                try:
                    notion_question_dict["category"] = Category.objects.get(
                        name=notion_question_dict["category"]
                    )
                except Category.DoesNotExist:
                    question_validation_errors.append(
                        ValidationError(
                            {
                                "category": f"Question {notion_question_dict['id']}."
                                f"Category '{notion_question_dict['category']}' inconnue"
                            }
                        )
                    )

            # cleanup relation tags
            # - if no tags, notion returns ['']
            # - check tags exist (then delete them to avoid errors)
            notion_question_tag_name_list = []
            if notion_question_dict["tags"] != [""]:
                notion_question_tag_name_list = [
                    tag
                    for tag in notion_question_dict["tags"]
                    if not tag.startswith("Quiz")
                ]
                new_tags = [
                    new_tag
                    for new_tag in notion_question_tag_name_list
                    if new_tag not in all_tags_list
                ]
                # missing tag error
                if len(new_tags):
                    question_validation_errors.append(
                        ValidationError(
                            {
                                "tags": f"Question {notion_question_dict['id']}."
                                f"Nouveau tag(s): {new_tags}"
                            }
                        )
                    )
            del notion_question_dict["tags"]

            # create or update
            # - if the question does not have validation_errors
            if len(question_validation_errors):
                validation_errors += question_validation_errors
            else:
                # if ("id" in notion_question_dict): # already checked above
                try:
                    db_question, created = Question.objects.get_or_create(
                        id=notion_question_dict["id"], defaults=notion_question_dict
                    )
                    # store info
                    if created:
                        notion_question_tag_objects = Tag.objects.filter(
                            name__in=notion_question_tag_name_list
                        )
                        db_question.tags.set(notion_question_tag_objects)
                        questions_created.append(db_question.id)
                    else:
                        # check possible changes
                        # basic fields
                        for question_model_field in Question._meta.get_fields():
                            if question_model_field.name in notion_question_dict:
                                # consider default values in some fields
                                if (
                                    (
                                        notion_question_dict[question_model_field.name]
                                        not in [None, ""]
                                    )
                                    and getattr(db_question, question_model_field.name)
                                    != notion_question_dict[question_model_field.name]
                                ) or (
                                    (
                                        notion_question_dict[question_model_field.name]
                                        in [None, ""]
                                    )
                                    and getattr(db_question, question_model_field.name)
                                    != question_model_field.get_default()
                                ):
                                    # track changes (before updating field to get previous value)
                                    db_question_field_update_message = f"Question {db_question.id} : champ '{question_model_field.name}' : {getattr(db_question, question_model_field.name)} >>> {notion_question_dict[question_model_field.name]}"  # noqa
                                    questions_updates.append(
                                        db_question_field_update_message
                                    )
                                    questions_updated.add(db_question.id)
                                    # update field
                                    setattr(
                                        db_question,
                                        question_model_field.name,
                                        notion_question_dict[question_model_field.name],
                                    )
                                    db_question.save(
                                        update_fields=[question_model_field.name]
                                    )
                        # tag field
                        has_different_tags = [
                            different_tag
                            for different_tag in notion_question_tag_name_list
                            if different_tag
                            not in list(db_question.tags.values_list("name", flat=True))
                        ]
                        if len(has_different_tags) or (
                            db_question.tags.count()
                            != len(notion_question_tag_name_list)
                        ):
                            # track changes
                            db_question_tag_update_message = f"Question {db_question.id} : champ 'tags' : {list(db_question.tags.values_list('name', flat=True))} >>> {notion_question_tag_name_list}"  # noqa
                            questions_updates.append(db_question_tag_update_message)
                            questions_updated.add(db_question.id)
                            # update tags
                            notion_question_tag_objects = Tag.objects.filter(
                                name__in=notion_question_tag_name_list
                            )
                            db_question.tags.set(notion_question_tag_objects)
                except ValidationError as e:
                    validation_errors.append(e)

        print("--- loop on questions : %s seconds ---" % (time.time() - start_time))
        start_time = time.time()

        # done
        questions_notion_count = (
            f"Nombre de questions dans Notion : {len(notion_questions_list)}"
        )
        questions_scope_count = f"Nombre de questions prises en compte ici (scope réduit ?) : {len(notion_questions_list_scope)}"  # noqa
        questions_ids_duplicate_message = f"ids 'en double' : {', '.join([str(question_id) for question_id in questions_ids_duplicate])}"  # noqa
        questions_ids_missing_message = f"ids 'manquants' : {', '.join([str(question_id) for question_id in questions_ids_missing])}"  # noqa

        questions_created_message = (
            f"Nombre de questions ajoutées : {len(questions_created)}"
        )
        if len(questions_created):
            questions_created_message += f" : {', '.join([str(question_id) for question_id in questions_created])}"  # noqa

        questions_updated_message = (
            f"Nombre de questions modifiées : {len(questions_updated)}"
        )
        if len(questions_updates):
            questions_updated_message += "|||" + "|||".join(questions_updates)

        validation_errors_message = (
            f"Erreurs : {len(validation_errors)}"
            + "|||"
            + "|||".join([str(error) for error in validation_errors])
            if len(validation_errors)
            else "aucune"
        )

        print("--- prints : %s seconds ---" % (time.time() - start_time))
        start_time = time.time()

        if not settings.DEBUG:
            utilities_notion.add_import_stats_row(
                len(notion_questions_list),
                len(questions_created),
                len(questions_updated),
            )

        print("--- send stats : %s seconds ---" % (time.time() - start_time))

        self.stdout.write(
            "|||".join(
                [
                    ">>> Info sur les questions",
                    questions_notion_count,
                    questions_scope_count,
                    questions_ids_duplicate_message,
                    questions_ids_missing_message,
                    "",
                    ">> Info sur les questions créés",
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
