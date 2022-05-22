# Generated by Django 4.1a1 on 2022-05-21 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("glossary", "0003_alter_glossaryitem_timestamps"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="glossaryitem",
            name="added",
        ),
        migrations.AddConstraint(
            model_name="glossaryitem",
            constraint=models.UniqueConstraint(fields=("name",), name="glossary_name_unique"),
        ),
    ]
