# Generated by Django 4.1.5 on 2023-03-10 16:03

import uuid

import ckeditor.fields
import django.contrib.postgres.fields
import django.db.models.deletion
import django.utils.timezone
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0007_authordetail"),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoricalAuthorDetail",
            fields=[
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
                ("image_url", models.URLField(blank=True, max_length=500, verbose_name="Author image (link)")),
                ("short_biography", ckeditor.fields.RichTextField(blank=True, verbose_name="Short biography")),
                (
                    "quiz_relationship",
                    ckeditor.fields.RichTextField(blank=True, verbose_name="Relationship with the Anthropocene Quiz"),
                ),
                ("website_url", models.URLField(blank=True, max_length=500, verbose_name="Website (link)")),
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
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical Author detail",
                "verbose_name_plural": "historical Author details",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
