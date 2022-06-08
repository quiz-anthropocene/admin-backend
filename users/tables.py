import django_tables2 as tables

from core.tables import DEFAULT_ATTRS, DEFAULT_TEMPLATE, ArrayColumn
from users.models import User


class ContributorTable(tables.Table):
    question_count = tables.Column(verbose_name="Questions")
    quiz_count = tables.Column(verbose_name="Quizs")
    roles = ArrayColumn()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "roles", "question_count", "quiz_count", "last_login", "created"]
        template_name = DEFAULT_TEMPLATE
        attrs = DEFAULT_ATTRS
