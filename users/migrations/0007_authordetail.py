# Generated by Django 4.1.5 on 2023-03-10 15:15

import ckeditor.fields
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_user_model_translation"),
    ]

    operations = [
        migrations.CreateModel(
            name="AuthorDetail",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
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
                ("updated", models.DateTimeField(auto_now=True, verbose_name="Last update date")),
            ],
            options={
                "verbose_name": "Author detail",
                "verbose_name_plural": "Author details",
            },
        ),
    ]
