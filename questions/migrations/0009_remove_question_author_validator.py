# Generated by Django 4.0.4 on 2022-05-07 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("questions", "0008_add_flatten_relation_fields"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="question",
            name="author_old",
        ),
        migrations.RemoveField(
            model_name="question",
            name="validator_old",
        ),
    ]
