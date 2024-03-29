# Generated by Django 4.1.5 on 2023-02-10 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("questions", "0017_rename_answer_audio_historicalquestion_answer_audio_url_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalquestion",
            name="answer_audio_url_text",
            field=models.CharField(
                blank=True, max_length=500, verbose_name="Texte pour remplacer l'affichage du lien 'explication audio'"
            ),
        ),
        migrations.AddField(
            model_name="historicalquestion",
            name="answer_video_url_text",
            field=models.CharField(
                blank=True, max_length=500, verbose_name="Texte pour remplacer l'affichage du lien 'explication vidéo'"
            ),
        ),
        migrations.AddField(
            model_name="question",
            name="answer_audio_url_text",
            field=models.CharField(
                blank=True, max_length=500, verbose_name="Texte pour remplacer l'affichage du lien 'explication audio'"
            ),
        ),
        migrations.AddField(
            model_name="question",
            name="answer_video_url_text",
            field=models.CharField(
                blank=True, max_length=500, verbose_name="Texte pour remplacer l'affichage du lien 'explication vidéo'"
            ),
        ),
    ]
