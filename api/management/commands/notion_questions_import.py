import notion
import collections

from django.core.management import BaseCommand
from django.core.exceptions import ValidationError

from api import utilities_notion
from api.models import Question, Category, Tag


class Command(BaseCommand):
    """
    Usage:
    - python manage.py notion_questions_import

    TODO: check id duplicates before
    """

    def handle(self, *args, **kwargs):
        notion_questions_list = []
        questions_ids_duplicate = []
        questions_ids_missing = []
        questions_created = []
        questions_updated = set()
        questions_updates = []
        validation_errors = []

        try:
            notion_questions_table = utilities_notion.get_questions_table()
            notion_questions_list = notion_questions_table.collection.get_rows()
        except:  # noqa
            self.stdout.write("Erreur accès Notion. token_v2 expiré ?")
            return
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

        for notion_question_row in notion_questions_list:
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
            # - field difficulty to int
            # - field added --> created time if none --> to date
            # - field validator --> "" if none
            if notion_question_dict["id"] is None:
                question_validation_errors.append(
                    ValidationError({"id": "Question sans id. vide ?"})
                )
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
                                "category": f"Question {notion_question_row.get_property('id')}."
                                f"Category '{notion_question_dict['category']}' inconnue"
                            }
                        )
                    )

            # cleanup relation tags
            # - if no tags, notion returns ['']
            # - check tags exist (then delete them to avoid errors)
            notion_question_tag_objects = []
            if notion_question_dict["tags"] != [""]:
                notion_question_dict["tags"] = [
                    tag
                    for tag in notion_question_dict["tags"]
                    if not tag.startswith("Quiz")
                ]
                notion_question_tag_objects = Tag.objects.filter(
                    name__in=notion_question_dict["tags"]
                )
                # missing tag error
                if (
                    len(notion_question_dict["tags"])
                    != notion_question_tag_objects.count()
                ):
                    tag_missing = [
                        tag
                        for tag in notion_question_dict["tags"]
                        if tag
                        not in list(
                            notion_question_tag_objects.values_list("name", flat=True)
                        )
                    ]
                    question_validation_errors.append(
                        ValidationError(
                            {
                                "tags": f"Question {notion_question_row.get_property('id')}."
                                f"nouveau tag(s): {tag_missing}"
                            }
                        )
                    )
            # TODO: check missing / new tags
            # error: Direct assignment to the forward side of a many-to-many set is prohibited. Use tags.set() instead.  # noqa
            # notion_question_dict["tags"] = Tag.objects.filter(name__in=notion_question_dict["tags"])  # noqa
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
                                    db_question_field_update_message = f"Question {db_question.id} : champ '{question_model_field.name}' : {getattr(db_question, question_model_field.name)} --> {notion_question_dict[question_model_field.name]}"  # noqa
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
                        if db_question.tags.count() != len(notion_question_tag_objects):
                            # track changes
                            db_question_tag_update_message = f"Question {db_question.id} : champ 'tags' : {list(db_question.tags.values_list('name', flat=True))} --> {list(notion_question_tag_objects.values_list('name', flat=True))}"  # noqa
                            questions_updates.append(db_question_tag_update_message)
                            questions_updated.add(db_question.id)
                            # update tags
                            db_question.tags.set(notion_question_tag_objects)
                except ValidationError as e:
                    validation_errors.append(e)

        # done
        questions_notion_info = f"Questions dans Notion : {len(notion_questions_list)}"
        questions_ids_duplicate_message = f"ids 'en double' : {', '.join([str(question_id) for question_id in questions_ids_duplicate])}"  # noqa
        questions_ids_missing_message = f"ids 'manquants' : {', '.join([str(question_id) for question_id in questions_ids_missing])}"  # noqa

        questions_created_message = f"Questions ajoutées : {len(questions_created)}"
        if len(questions_created):
            questions_created_message += f" : {', '.join([str(question_id) for question_id in questions_created])}"  # noqa

        questions_updated_message = f"Questions modifiées : {len(questions_updated)}"
        questions_updates_message = "\n".join(questions_updates)

        validation_errors_message = (
            f"Erreurs : {len(validation_errors)}"
            + "\n"
            + "\n".join([str(error) for error in validation_errors])
            if len(validation_errors)
            else "aucune"
        )

        self.stdout.write(
            "\n".join(
                [
                    ">>> Info sur les questions",
                    questions_notion_info,
                    questions_ids_duplicate_message,
                    questions_ids_missing_message,
                    "",
                    ">> Info sur les questions créés",
                    questions_created_message,
                    "",
                    ">>> Info sur les questions modifiées",
                    questions_updated_message,
                    questions_updates_message,
                    "",
                    ">>> Erreurs lors de l'import",
                    validation_errors_message,
                ]
            )
        )
