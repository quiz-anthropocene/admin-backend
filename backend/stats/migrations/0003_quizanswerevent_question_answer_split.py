# Generated by Django 4.0.3 on 2022-04-19 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0002_questionanswerevent_quiz_questionfeedbackevent_quiz"),
    ]

    operations = [
        migrations.AddField(
            model_name="quizanswerevent",
            name="question_answer_split",
            field=models.JSONField(default=dict, help_text="Les détails par question"),
        ),
    ]