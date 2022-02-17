# Generated by Django 3.1.4 on 2021-02-22 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0078_auto_20210222_0924"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="language",
            field=models.CharField(
                choices=[("Français", "Français"), ("English", "English")],
                default="Français",
                help_text="La langue de la question",
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="quiz",
            name="language",
            field=models.CharField(
                choices=[("Français", "Français"), ("English", "English")],
                default="Français",
                help_text="La langue du quiz",
                max_length=50,
            ),
        ),
    ]