# Generated by Django 4.0.3 on 2022-03-27 19:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("questions", "0001_initial"),
        ("stats", "0006_alter_quizanswerevent_quiz_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="questionaggstat",
            name="question",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                primary_key=True,
                related_name="agg_stats",
                serialize=False,
                to="questions.question",
            ),
        ),
        migrations.AlterField(
            model_name="questionanswerevent",
            name="question",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, related_name="stats", to="questions.question"
            ),
        ),
        migrations.AlterField(
            model_name="questionfeedbackevent",
            name="question",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="feedbacks",
                to="questions.question",
            ),
        ),
    ]
