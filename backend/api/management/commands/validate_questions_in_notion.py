import notion
from django.core.exceptions import ValidationError
from django.core.management import BaseCommand

from api import utilities_notion
from api.models import Question, Tag
from categories.models import Category


class Command(BaseCommand):
    """
    Usage:
    - python manage.py validate_questions_in_notion
    """

    def handle(self, *args, **kwargs):
        validation_errors = []

        notion_questions_table = utilities_notion.get_questions_table()
        notion_questions_list = notion_questions_table.collection.get_rows()

        for notion_question_row in notion_questions_list:
            notion_question_dict = dict()

            # fill dict with notion_question_row
            for question_field in Question._meta.get_fields():
                try:
                    notion_question_property = notion_question_row.get_property(question_field.name)
                    # cleanup dates
                    if type(notion_question_property) == notion.collection.NotionDate:
                        notion_question_property = notion_question_property.start
                    # skip empty values (se baser sur les defaults plutot)
                    if notion_question_property not in ["", None, [], [""]]:
                        notion_question_dict[question_field.name] = notion_question_property
                except:  # noqa
                    pass

            # cleanup
            # - avoid id unique rule
            # - check category exists
            # - check tags exist (then delete them)
            if "id" not in notion_question_dict:
                validation_errors.append(ValidationError({"id": "Question sans id. vide ?"}))
            else:
                notion_question_dict["id"] += 10000
            if "category" in notion_question_dict:
                # error if unknown category : api.models.DoesNotExist: Category matching query does not exist.  # noqa
                notion_question_dict["category"] = Category.objects.get(name=notion_question_dict["category"])
            if "tags" in notion_question_dict:
                notion_question_dict["tags"] = [
                    tag for tag in notion_question_dict["tags"] if not tag.startswith("Quiz")
                ]
                tag_list = Tag.objects.filter(name__in=notion_question_dict["tags"]).values_list("name", flat=True)
                if len(notion_question_dict["tags"]) != tag_list.count():
                    tag_missing = [tag for tag in notion_question_dict["tags"] if tag not in list(tag_list)]
                    validation_errors.append(
                        ValidationError(
                            {
                                "tags": f"Question {notion_question_row.get_property('id')}. nouveau tag(s): {tag_missing}"  # noqa
                            }
                        )
                    )
                # TODO: check missing / new tags
                # error: Direct assignment to the forward side of a many-to-many set is prohibited. Use tags.set() instead.  # noqa
                # notion_question_dict["tags"] = Tag.objects.filter(name__in=notion_question_dict["tags"])  # noqa
                del notion_question_dict["tags"]

            # validate
            notion_question = Question(**notion_question_dict)
            try:
                notion_question.full_clean()
            except ValidationError as e:
                validation_errors.append(e)

        # done
        print(validation_errors)
        # self.stdout.write(validation_errors)
        if len(validation_errors):
            self.stdout.write("\n".join([str(error) for error in validation_errors]))
        else:
            self.stdout.write("pas d'erreurs")
