# Generated by Django 4.1.5 on 2023-02-24 19:45

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("activity", "0002_alter_event_created_alter_event_event_object_type"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="event",
            options={"verbose_name": "Event", "verbose_name_plural": "Events"},
        ),
        migrations.AlterField(
            model_name="event",
            name="actor_id",
            field=models.IntegerField(blank=True, verbose_name="Actor ID"),
        ),
        migrations.AlterField(
            model_name="event",
            name="actor_name",
            field=models.CharField(blank=True, max_length=150, verbose_name="Actor name"),
        ),
        migrations.AlterField(
            model_name="event",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name="Creation date"),
        ),
        migrations.AlterField(
            model_name="event",
            name="event_object_id",
            field=models.IntegerField(blank=True, verbose_name="Object ID"),
        ),
        migrations.AlterField(
            model_name="event",
            name="event_object_name",
            field=models.CharField(blank=True, max_length=150, verbose_name="Object name"),
        ),
        migrations.AlterField(
            model_name="event",
            name="event_object_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("QUESTION", "Question"),
                    ("QUIZ", "Quiz"),
                    ("USER", "Contributor"),
                    ("WEEKLY_AGG_STAT", "Weekly statistics"),
                ],
                max_length=50,
                verbose_name="Object type",
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="event_verb",
            field=models.CharField(
                blank=True,
                choices=[
                    ("CREATED", "Created"),
                    ("UPDATED", "Updated"),
                    ("VALIDATED", "Validated"),
                    ("PUBLISHED", "Published"),
                    ("DELETED", "Deleted"),
                    ("COMPUTED", "Computed"),
                ],
                max_length=50,
                verbose_name="Verb",
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="extra_data",
            field=models.JSONField(default=dict, verbose_name="Additional data"),
        ),
    ]