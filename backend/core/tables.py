import django_tables2 as tables
from django.utils.html import format_html

from core import constants
from core.utils.utilities import get_choice_key
from questions.models import Question


class ChoiceColumn(tables.Column):
    def render(self, value, record, bound_column):
        value_title = value
        if type(record) == Question:
            if bound_column.name == "type":
                value_title = value
                value = get_choice_key(constants.QUESTION_TYPE_CHOICES, value)
        return format_html(f'<span class="badge bg-primary" title="{value_title}">{value}</span>')


class ImageColumn(tables.Column):
    def render(self, value):
        return format_html(
            f'<a href="{value}" target="_blank">' f'<img src="{value}" title="{value}" height="100" />' f"</a>"
        )


class LongTextEllipsisColumn(tables.Column):
    def render(self, value):
        if len(value) > 60:
            value = value[:54] + " (...)"
        return format_html(value)
