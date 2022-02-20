# Generated by Django 3.0.4 on 2020-05-24 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0034_rename_model_stats"),
    ]

    operations = [
        migrations.CreateModel(
            name="QuizFeedbackEvent",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "choice",
                    models.CharField(
                        choices=[("like", "Positif"), ("dislike", "Négatif")],
                        default="like",
                        editable=False,
                        help_text="L'avis laissé sur le quiz",
                        max_length=50,
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, help_text="La date & heure de l'avis"
                    ),
                ),
                (
                    "quiz",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="feedbacks",
                        to="api.Quiz",
                    ),
                ),
            ],
        ),
    ]