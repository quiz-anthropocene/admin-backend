# Generated by Django 4.0.4 on 2022-05-04 13:10

import uuid

import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("categories", "0003_alter_category_timestamps"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("questions", "0006_rename_question_author_validator"),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoricalQuestion",
            fields=[
                ("id", models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name="ID")),
                (
                    "text",
                    models.TextField(
                        help_text="Rechercher la simplicité, faire des phrases courtes", verbose_name="Texte"
                    ),
                ),
                (
                    "hint",
                    models.TextField(
                        blank=True,
                        help_text="L'utilisateur pourra décider de l'afficher pour l'aider",
                        verbose_name="Indice",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("QCM", "Questionnaire à choix multiples"),
                            ("QCM-RM", "Questionnaire à choix multiples avec réponses multiples"),
                            ("VF", "Vrai ou Faux"),
                        ],
                        default="QCM",
                        max_length=50,
                        verbose_name="Type",
                    ),
                ),
                (
                    "difficulty",
                    models.IntegerField(
                        choices=[(0, "Junior"), (1, "Facile"), (2, "Moyen"), (3, "Difficile"), (4, "Expert")],
                        default=1,
                        verbose_name="Niveau de difficulté",
                    ),
                ),
                (
                    "language",
                    models.CharField(
                        choices=[("Français", "Français"), ("English", "English")],
                        default="Français",
                        max_length=50,
                        verbose_name="Langue",
                    ),
                ),
                ("answer_option_a", models.CharField(blank=True, max_length=500, verbose_name="La réponse a")),
                ("answer_option_b", models.CharField(blank=True, max_length=500, verbose_name="La réponse b")),
                ("answer_option_c", models.CharField(blank=True, max_length=500, verbose_name="La réponse c")),
                ("answer_option_d", models.CharField(blank=True, max_length=500, verbose_name="La réponse d")),
                (
                    "answer_correct",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("a", "a"),
                            ("b", "b"),
                            ("c", "c"),
                            ("d", "d"),
                            ("ab", "ab"),
                            ("ac", "ac"),
                            ("ad", "ad"),
                            ("bc", "bc"),
                            ("bd", "bd"),
                            ("cd", "cd"),
                            ("abc", "abc"),
                            ("abd", "abd"),
                            ("acd", "acd"),
                            ("bcd", "bcd"),
                            ("abcd", "abcd"),
                        ],
                        help_text="a, b, c ou d. ab, acd, abcd… si plusieurs réponses.",
                        max_length=50,
                        verbose_name="La bonne réponse",
                    ),
                ),
                (
                    "has_ordered_answers",
                    models.BooleanField(
                        default=True,
                        help_text="Les choix de réponse sont affichés dans cet ordre, et ne doivent pas être mélangés",
                        verbose_name="Réponses ordonnées ?",
                    ),
                ),
                (
                    "answer_explanation",
                    models.TextField(blank=True, verbose_name="Explication de texte de la bonne réponse"),
                ),
                (
                    "answer_audio",
                    models.URLField(blank=True, max_length=500, verbose_name="Lien vers une explication audio"),
                ),
                (
                    "answer_video",
                    models.URLField(blank=True, max_length=500, verbose_name="Lien vers une explication vidéo"),
                ),
                (
                    "answer_accessible_url",
                    models.URLField(blank=True, max_length=500, verbose_name="Lien vers une source 'grand public'"),
                ),
                (
                    "answer_accessible_url_text",
                    models.CharField(
                        blank=True,
                        max_length=500,
                        verbose_name="Texte pour remplacer l'affichage du lien 'grand public'",
                    ),
                ),
                (
                    "answer_scientific_url",
                    models.URLField(
                        blank=True,
                        help_text="Rapport, article en anglais…",
                        max_length=500,
                        verbose_name="Lien vers une source 'scientifique'",
                    ),
                ),
                (
                    "answer_scientific_url_text",
                    models.CharField(
                        blank=True,
                        max_length=500,
                        verbose_name="Texte pour remplacer l'affichage du lien 'scientifique'",
                    ),
                ),
                (
                    "answer_reading_recommendation",
                    models.TextField(blank=True, verbose_name="Un livre pour aller plus loin"),
                ),
                (
                    "answer_image_url",
                    models.URLField(
                        blank=True, max_length=500, verbose_name="Lien vers une image pour illustrer la réponse"
                    ),
                ),
                (
                    "answer_image_explanation",
                    models.TextField(
                        blank=True,
                        help_text="Légende, traduction, explication courte…",
                        verbose_name="Texte explicatif pour l'image",
                    ),
                ),
                (
                    "answer_extra_info",
                    models.TextField(
                        blank=True,
                        help_text="Ne s'affichera pas dans l'application",
                        verbose_name="Notes, commentaires et liens explicatifs additionels",
                    ),
                ),
                (
                    "validation_status",
                    models.CharField(
                        choices=[
                            ("Brouillon", "Brouillon"),
                            ("A valider", "A valider"),
                            ("Validée", "Validée"),
                            ("Écartée temporairement", "Écartée temporairement"),
                            ("Écartée", "Écartée"),
                        ],
                        default="Brouillon",
                        max_length=150,
                        verbose_name="Statut",
                    ),
                ),
                ("added", models.DateField(blank=True, null=True, verbose_name="Date d'ajout")),
                ("created", models.DateTimeField(blank=True, editable=False, verbose_name="Date de création")),
                (
                    "updated",
                    models.DateTimeField(blank=True, editable=False, verbose_name="Date de dernière modification"),
                ),
                (
                    "history_id",
                    models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
                ),
                ("history_date", models.DateTimeField()),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")], max_length=1),
                ),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Auteur",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="categories.category",
                        verbose_name="Catégorie",
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "validator",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Validateur",
                    ),
                ),
            ],
            options={
                "verbose_name": "historical Question",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": "history_date",
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
