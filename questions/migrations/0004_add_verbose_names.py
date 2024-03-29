# Generated by Django 4.0.4 on 2022-04-30 16:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tags", "0002_add_verbose_names"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("categories", "0002_add_verbose_names"),
        ("questions", "0003_populate_question_author_link_and_validator_link"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="added",
            field=models.DateField(blank=True, null=True, verbose_name="Date d'ajout"),
        ),
        migrations.AlterField(
            model_name="question",
            name="answer_accessible_url",
            field=models.URLField(blank=True, max_length=500, verbose_name="Lien vers une source 'grand public'"),
        ),
        migrations.AlterField(
            model_name="question",
            name="answer_accessible_url_text",
            field=models.CharField(
                blank=True, max_length=500, verbose_name="Texte pour remplacer l'affichage du lien 'grand public'"
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="answer_audio",
            field=models.URLField(blank=True, max_length=500, verbose_name="Lien vers une explication audio"),
        ),
        migrations.AlterField(
            model_name="question",
            name="answer_correct",
            field=models.CharField(
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
        migrations.AlterField(
            model_name="question",
            name="answer_explanation",
            field=models.TextField(blank=True, verbose_name="Explication de texte de la bonne réponse"),
        ),
        migrations.AlterField(
            model_name="question",
            name="answer_extra_info",
            field=models.TextField(
                blank=True,
                help_text="Ne s'affichera pas dans l'application",
                verbose_name="Notes, commentaires et liens explicatifs additionels",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="answer_image_explanation",
            field=models.TextField(
                blank=True,
                help_text="Légende, traduction, explication courte…",
                verbose_name="Texte explicatif pour l'image",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="answer_image_url",
            field=models.URLField(
                blank=True, max_length=500, verbose_name="Lien vers une image pour illustrer la réponse"
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="answer_option_a",
            field=models.CharField(blank=True, max_length=500, verbose_name="La réponse a"),
        ),
        migrations.AlterField(
            model_name="question",
            name="answer_option_b",
            field=models.CharField(blank=True, max_length=500, verbose_name="La réponse b"),
        ),
        migrations.AlterField(
            model_name="question",
            name="answer_option_c",
            field=models.CharField(blank=True, max_length=500, verbose_name="La réponse c"),
        ),
        migrations.AlterField(
            model_name="question",
            name="answer_option_d",
            field=models.CharField(blank=True, max_length=500, verbose_name="La réponse d"),
        ),
        migrations.AlterField(
            model_name="question",
            name="answer_reading_recommendation",
            field=models.TextField(blank=True, verbose_name="Un livre pour aller plus loin"),
        ),
        migrations.AlterField(
            model_name="question",
            name="answer_scientific_url",
            field=models.URLField(
                blank=True,
                help_text="Rapport, article en anglais…",
                max_length=500,
                verbose_name="Lien vers une source 'scientifique'",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="answer_scientific_url_text",
            field=models.CharField(
                blank=True, max_length=500, verbose_name="Texte pour remplacer l'affichage du lien 'scientifique'"
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="answer_video",
            field=models.URLField(blank=True, max_length=500, verbose_name="Lien vers une explication vidéo"),
        ),
        migrations.AlterField(
            model_name="question",
            name="author",
            field=models.CharField(blank=True, max_length=50, verbose_name="Auteur"),
        ),
        migrations.AlterField(
            model_name="question",
            name="author_link",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="questions",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Auteur",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="questions",
                to="categories.category",
                verbose_name="Catégorie",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="created",
            field=models.DateField(auto_now_add=True, verbose_name="Date de création"),
        ),
        migrations.AlterField(
            model_name="question",
            name="difficulty",
            field=models.IntegerField(
                choices=[(0, "Junior"), (1, "Facile"), (2, "Moyen"), (3, "Difficile"), (4, "Expert")],
                default=1,
                verbose_name="Niveau de difficulté",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="has_ordered_answers",
            field=models.BooleanField(
                default=True,
                help_text="Les choix de réponse sont affichés dans cet ordre, et ne doivent pas être mélangés",
                verbose_name="Réponses ordonnées ?",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="hint",
            field=models.TextField(
                blank=True, help_text="L'utilisateur pourra décider de l'afficher pour l'aider", verbose_name="Indice"
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="language",
            field=models.CharField(
                choices=[("Français", "Français"), ("English", "English")],
                default="Français",
                max_length=50,
                verbose_name="Langue",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="tags",
            field=models.ManyToManyField(blank=True, related_name="questions", to="tags.tag", verbose_name="Tag(s)"),
        ),
        migrations.AlterField(
            model_name="question",
            name="text",
            field=models.TextField(
                help_text="Rechercher la simplicité, faire des phrases courtes", verbose_name="Texte"
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="type",
            field=models.CharField(
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
        migrations.AlterField(
            model_name="question",
            name="updated",
            field=models.DateField(auto_now=True, verbose_name="Date de dernière modification"),
        ),
        migrations.AlterField(
            model_name="question",
            name="validation_status",
            field=models.CharField(
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
        migrations.AlterField(
            model_name="question",
            name="validator",
            field=models.CharField(blank=True, max_length=50, verbose_name="Validateur"),
        ),
        migrations.AlterField(
            model_name="question",
            name="validator_link",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="questions_validated",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Validateur",
            ),
        ),
    ]
