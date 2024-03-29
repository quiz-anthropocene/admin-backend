# Generated by Django 4.0.4 on 2022-05-05 09:15

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tags", "0003_alter_tag_timestamps"),
        ("quizs", "0007_historicalquiz"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalquiz",
            name="author_string",
            field=models.CharField(blank=True, max_length=300, verbose_name="Auteur"),
        ),
        migrations.AddField(
            model_name="historicalquiz",
            name="question_list",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.PositiveIntegerField(), blank=True, default=list, size=None, verbose_name="Questions"
            ),
        ),
        migrations.AddField(
            model_name="historicalquiz",
            name="relationship_list",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=50),
                blank=True,
                default=list,
                size=None,
                verbose_name="Relations",
            ),
        ),
        migrations.AddField(
            model_name="historicalquiz",
            name="tag_list",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=50), blank=True, default=list, size=None, verbose_name="Tags"
            ),
        ),
        migrations.AddField(
            model_name="quiz",
            name="author_string",
            field=models.CharField(blank=True, max_length=300, verbose_name="Auteur"),
        ),
        migrations.AddField(
            model_name="quiz",
            name="question_list",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.PositiveIntegerField(), blank=True, default=list, size=None, verbose_name="Questions"
            ),
        ),
        migrations.AddField(
            model_name="quiz",
            name="relationship_list",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=50),
                blank=True,
                default=list,
                size=None,
                verbose_name="Relations",
            ),
        ),
        migrations.AddField(
            model_name="quiz",
            name="tag_list",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=50), blank=True, default=list, size=None, verbose_name="Tags"
            ),
        ),
        migrations.AlterField(
            model_name="quiz",
            name="tags",
            field=models.ManyToManyField(blank=True, related_name="quizs", to="tags.tag", verbose_name="Tags"),
        ),
        migrations.AlterField(
            model_name="quiz",
            name="questions",
            field=models.ManyToManyField(
                related_name="quizs", through="quizs.QuizQuestion", to="questions.question", verbose_name="Questions"
            ),
        ),
    ]
