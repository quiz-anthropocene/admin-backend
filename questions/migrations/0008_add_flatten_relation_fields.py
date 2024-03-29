# Generated by Django 4.0.4 on 2022-05-05 07:47

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("questions", "0007_historicalquestion"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalquestion",
            name="author_string",
            field=models.CharField(blank=True, max_length=300, verbose_name="Auteur"),
        ),
        migrations.AddField(
            model_name="historicalquestion",
            name="category_string",
            field=models.CharField(blank=True, max_length=50, verbose_name="Catégorie"),
        ),
        migrations.AddField(
            model_name="historicalquestion",
            name="tag_list",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=50), blank=True, default=list, size=None, verbose_name="Tags"
            ),
        ),
        migrations.AddField(
            model_name="historicalquestion",
            name="quiz_list",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.PositiveIntegerField(), blank=True, default=list, size=None, verbose_name="Quizs"
            ),
        ),
        migrations.AddField(
            model_name="historicalquestion",
            name="validator_string",
            field=models.CharField(blank=True, max_length=300, verbose_name="Validateur"),
        ),
        migrations.AddField(
            model_name="question",
            name="author_string",
            field=models.CharField(blank=True, max_length=300, verbose_name="Auteur"),
        ),
        migrations.AddField(
            model_name="question",
            name="category_string",
            field=models.CharField(blank=True, max_length=50, verbose_name="Catégorie"),
        ),
        migrations.AddField(
            model_name="question",
            name="tag_list",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=50), blank=True, default=list, size=None, verbose_name="Tags"
            ),
        ),
        migrations.AddField(
            model_name="question",
            name="validator_string",
            field=models.CharField(blank=True, max_length=300, verbose_name="Validateur"),
        ),
        migrations.AlterField(
            model_name="question",
            name="tags",
            field=models.ManyToManyField(blank=True, related_name="questions", to="tags.tag", verbose_name="Tags"),
        ),
        migrations.AddField(
            model_name="question",
            name="quiz_list",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.PositiveIntegerField(), blank=True, default=list, size=None, verbose_name="Quizs"
            ),
        ),
    ]
