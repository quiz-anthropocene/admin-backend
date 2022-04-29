import django_tables2 as tables

from core.tables import ArrayColumn
from users.models import User


class ContributorTable(tables.Table):
    question_count = tables.Column(verbose_name="Questions")
    quiz_count = tables.Column(verbose_name="Quizs")
    roles = ArrayColumn()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "question_count", "quiz_count", "roles", "last_login", "created"]
        template_name = "django_tables2/bootstrap4.html"
        attrs = {"class": "table-responsive table-striped table-bordered border-primary font-size-small"}
