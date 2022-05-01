import django_tables2 as tables
from django.utils.encoding import force_str
from django.utils.html import format_html

from core import constants
from core.utils.utilities import get_choice_key
from questions.models import Question
from users import constants as user_constants
from users.models import User


class ChoiceColumn(tables.Column):
    def render(self, value, record, bound_column):
        value_title = value
        if type(record) == Question:
            # Question.type : display choice key
            if bound_column.name == "type":
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
        if type(record) == User:
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
        return format_html(value)


class RichTextEllipsisColumn(tables.Column):
    def render(self, value):
        if len(value) > 60:
            value = value[:54] + " (…)"
        return format_html(value)
