# Generated by Django 4.1 on 2022-08-17 14:19

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0004_dailystat_question_public_and_quiz_public_answer_count"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dailystat",
            name="created",
            field=models.DateTimeField(
                default=django.utils.timezone.now, help_text="La date & heure de la stat journalière"
            ),
        ),
        migrations.AlterField(
            model_name="questionanswerevent",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now, help_text="La date & heure de la réponse"),
        ),
        migrations.AlterField(
            model_name="questionfeedbackevent",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now, help_text="La date & heure de l'avis"),
        ),
        migrations.AlterField(
            model_name="quizanswerevent",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now, help_text="La date & heure de la réponse"),
        ),
        migrations.AlterField(
            model_name="quizfeedbackevent",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now, help_text="La date & heure de l'avis"),
        ),
    ]
