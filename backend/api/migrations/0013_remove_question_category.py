# Generated by Django 3.0.4 on 2020-04-05 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0012_question_category_temp"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="question",
            name="category",
        ),
    ]
