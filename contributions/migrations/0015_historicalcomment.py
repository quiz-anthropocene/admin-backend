# Generated by Django 4.1.5 on 2023-03-21 15:43

import uuid

import django.contrib.postgres.fields
import django.db.models.deletion
import django.utils.timezone
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("questions", "0028_alter_historicalquestion_history_changed_fields"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("quizs", "0028_alter_historicalquiz_history_changed_fields"),
        ("contributions", "0014_comment_remove_status_replied"),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoricalComment",
            fields=[
                ("id", models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name="ID")),
                (
                    "history_changed_fields",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=50),
                        blank=True,
                        default=list,
                        size=None,
                        verbose_name="Changed fields",
                    ),
                ),
                ("text", models.TextField(help_text="A question, a comment…", verbose_name="Text")),
                ("description", models.TextField(blank=True, verbose_name="Additional information")),
                (
                    "type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("NEW_QUESTION", "New question"),
                            ("NEW_QUIZ", "New quiz"),
                            ("COMMENT_APP", "Comment about the app"),
                            ("COMMENT_QUESTION", "Comment about a question"),
                            ("COMMENT_QUIZ", "Comment about a quiz"),
                            ("COMMENT_CONTRIBUTOR", "Contributor note"),
                            ("REPLY", "Reply"),
                            ("ERROR_APP", "Application error"),
                        ],
                        max_length=150,
                        verbose_name="Type",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("NEW", "To process"),
                            ("PENDING", "In progress"),
                            ("PROCESSED", "Processed"),
                            ("IGNORED", "Ignored"),
                        ],
                        max_length=150,
                        verbose_name="Status",
                    ),
                ),
                ("created", models.DateTimeField(default=django.utils.timezone.now, verbose_name="Creation date")),
                ("updated", models.DateTimeField(blank=True, editable=False, verbose_name="Last update date")),
                (
                    "history_id",
                    models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
                ),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")], max_length=1),
                ),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Author",
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="contributions.comment",
                        verbose_name="In reply to",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="questions.question",
                        verbose_name="Question",
                    ),
                ),
                (
                    "quiz",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="quizs.quiz",
                        verbose_name="Quiz",
                    ),
                ),
            ],
            options={
                "verbose_name": "historical Comment",
                "verbose_name_plural": "historical Comments",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
