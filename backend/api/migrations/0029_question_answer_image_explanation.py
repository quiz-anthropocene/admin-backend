# Generated by Django 3.0.4 on 2020-05-11 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0028_auto_20200505_0817"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="answer_image_explanation",
            field=models.TextField(blank=True, help_text="Une légende pour l'image qui illustre la réponse"),
        ),
    ]
