# Generated by Django 4.0.4 on 2022-05-01 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quizs", "0004_add_verbose_names"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quiz",
            name="created",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Date de création"),
        ),
        migrations.AlterField(
            model_name="quiz",
            name="updated",
            field=models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification"),
        ),
        migrations.AlterField(
            model_name="quizquestion",
            name="created",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Date de création"),
        ),
        migrations.AlterField(
            model_name="quizquestion",
            name="updated",
            field=models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification"),
        ),
        migrations.AlterField(
            model_name="quizrelationship",
            name="created",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Date de création"),
        ),
    ]