# Generated by Django 4.0.4 on 2022-05-11 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0003_quizanswerevent_question_answer_split"),
    ]

    operations = [
        migrations.AddField(
            model_name="dailystat",
            name="question_public_answer_count",
            field=models.PositiveIntegerField(default=0, help_text="Le nombre de questions publiques répondues"),
        ),
        migrations.AddField(
            model_name="dailystat",
            name="quiz_public_answer_count",
            field=models.PositiveIntegerField(default=0, help_text="Le nombre de quizs publiques répondus"),
        ),
    ]