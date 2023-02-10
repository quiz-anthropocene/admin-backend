# Generated by Django 4.1.5 on 2023-01-27 14:40

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("questions", "0017_rename_answer_audio_historicalquestion_answer_audio_url_and_more"),
        ("quizs", "0020_remove_historicalquiz_author_and_more"),
        ("stats", "0005_alter_dailystat_created_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="LinkClickEvent",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("link_url", models.URLField(blank=True, max_length=500, verbose_name="Lien cliqué")),
                (
                    "created",
                    models.DateTimeField(default=django.utils.timezone.now, help_text="La date & heure du clic"),
                ),
                (
                    "question",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="link_clicks",
                        to="questions.question",
                    ),
                ),
                (
                    "quiz",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="link_clicks",
                        to="quizs.quiz",
                    ),
                ),
            ],
        ),
    ]