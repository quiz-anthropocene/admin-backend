# Generated by Django 4.0.3 on 2022-03-27 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0090_alter_question_category"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="question",
            name="tags",
        ),
        migrations.RemoveField(
            model_name="quiz",
            name="tags",
        ),
        migrations.DeleteModel(
            name="Tag",
        ),
    ]