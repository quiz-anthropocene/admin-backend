# Generated by Django 3.1.1 on 2020-11-19 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0051_update_django_jsonfield"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"ordering": ["pk"]},
        ),
        migrations.AlterModelOptions(
            name="question",
            options={"ordering": ["pk"]},
        ),
        migrations.AlterModelOptions(
            name="quiz",
            options={"ordering": ["pk"]},
        ),
        migrations.AlterModelOptions(
            name="tag",
            options={"ordering": ["pk"]},
        ),
        migrations.RemoveConstraint(
            model_name="glossary",
            name="unique glossary name",
        ),
    ]
