# Generated by Django 4.1.5 on 2023-03-20 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("contributions", "0013_rename_comment_fks"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={"ordering": ["-created"], "verbose_name": "Comment", "verbose_name_plural": "Comments"},
        ),
    ]
