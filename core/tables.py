import django_tables2 as tables
from django.utils.encoding import force_str
from django.utils.html import format_html

from core import constants
from core.utils.utilities import get_choice_key, remove_html_tags, truncate_with_ellipsis
from questions.models import Question
from quizs.models import QuizQuestion
from users import constants as user_constants
from users.models import User


DEFAULT_TEMPLATE = "django_tables2/bootstrap4.html"
DEFAULT_ATTRS = {"class": "table-responsive table-striped table-bordered border-primary font-size-small"}


class ChoiceColumn(tables.Column):
    def render(self, value, record, bound_column):
        value_title = value
        if type(record) in [Question, QuizQuestion]:
            # Question.type : display choice key instead of value
            if bound_column.name in ["type", "question_type"]:
                value_title = value
                value = get_choice_key(constants.QUESTION_TYPE_CHOICES, value)
            # Question.category : add link
            elif bound_column.name == "category":
                category = getattr(record, bound_column.name)
                return format_html(
                    f'<a href="{category.get_absolute_url()}">'
                    f'<span class="badge bg-primary" title="{value_title}">{value}</span>'
                    "</a>"
                )
        return format_html(f'<span class="badge bg-primary" title="{value_title}">{value}</span>')


class ArrayColumn(tables.Column):
    def render(self, value, record, bound_column):
        output_array = list()
        if type(record) is User:
            if bound_column.name == "roles":
                choices_dict = dict(user_constants.USER_ROLE_CHOICES)
                for item in value:
                    output_array.append(
                        f'<span class="badge bg-primary">{force_str(choices_dict.get(item, ""))}</span>'
                    )
        else:
            for item in value:
                output_array.append(f'<span class="badge bg-primary">{item}</span>')
        return format_html(" ".join(output_array))


class ImageColumn(tables.Column):
    def render(self, value):
        return format_html(
            f'<a href="{value}" target="_blank" rel="noopener"><img src="{value}" title="{value}" height="100" /></a>'
        )


class RichTextColumn(tables.Column):
    def render(self, value):
        # could have used format_html or strip_tags
        return remove_html_tags(value)


class RichTextEllipsisColumn(tables.Column):
    def render(self, value):
        value_cleaned = remove_html_tags(value)
        return truncate_with_ellipsis(value_cleaned, 60)


class RichTextLongerEllipsisColumn(tables.Column):
    def render(self, value):
        value_cleaned = remove_html_tags(value)
        return truncate_with_ellipsis(value_cleaned, 300)
