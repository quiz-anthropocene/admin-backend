# Generated by Django 4.2 on 2023-06-23 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0008_historicalusercard"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="logs",
            field=models.JSONField(default=list, editable=False, verbose_name="Logs historiques"),
        ),
    ]
