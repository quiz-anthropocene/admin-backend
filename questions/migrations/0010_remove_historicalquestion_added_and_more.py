# Generated by Django 4.0.4 on 2022-05-07 22:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("questions", "0009_remove_question_author_validator"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicalquestion",
            name="added",
        ),
        migrations.RemoveField(
            model_name="question",
            name="added",
        ),
    ]
