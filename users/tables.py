import django_tables2 as tables

from core.tables import DEFAULT_ATTRS, DEFAULT_TEMPLATE, ArrayColumn
from questions.models import Question
from quizs.models import Quiz
from users.models import User


class ContributorTable(tables.Table):
    question_count = tables.Column(verbose_name=Question._meta.verbose_name_plural)
    quiz_count = tables.Column(verbose_name=Quiz._meta.verbose_name_plural)
    roles = ArrayColumn()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "roles", "question_count", "quiz_count", "last_login", "created"]
        template_name = DEFAULT_TEMPLATE
        attrs = DEFAULT_ATTRS


class AdministratorTable(tables.Table):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "last_login"]
        template_name = DEFAULT_TEMPLATE
        attrs = DEFAULT_ATTRS
