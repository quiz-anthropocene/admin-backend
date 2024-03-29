# Generated by Django 4.0.4 on 2022-05-08 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quizs", "0009_remove_quiz_author"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalquiz",
            name="visibility",
            field=models.CharField(
                choices=[
                    ("PUBLIC", "Publique (dans l'export et dans l'application)"),
                    ("HIDDEN", "Caché (dans l'export mais pas visible dans l'application)"),
                    ("PRIVATE", "Privé (pas dans l'export ni dans l'application)"),
                ],
                default="PUBLIC",
                max_length=50,
                verbose_name="Visibilité",
            ),
        ),
        migrations.AddField(
            model_name="quiz",
            name="visibility",
            field=models.CharField(
                choices=[
                    ("PUBLIC", "Publique (dans l'export et dans l'application)"),
                    ("HIDDEN", "Caché (dans l'export mais pas visible dans l'application)"),
                    ("PRIVATE", "Privé (pas dans l'export ni dans l'application)"),
                ],
                default="PUBLIC",
                max_length=50,
                verbose_name="Visibilité",
            ),
        ),
    ]
