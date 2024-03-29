# Generated by Django 4.2 on 2023-04-28 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("activity", "0003_event_model_translate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="actor_id",
            field=models.IntegerField(blank=True, null=True, verbose_name="Actor ID"),
        ),
        migrations.AlterField(
            model_name="event",
            name="event_object_id",
            field=models.IntegerField(blank=True, null=True, verbose_name="Object ID"),
        ),
    ]
