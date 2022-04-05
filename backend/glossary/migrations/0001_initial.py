# Generated by Django 4.0.3 on 2022-03-30 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="GlossaryItem",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(help_text="Le mot ou sigle", max_length=50)),
                ("name_alternatives", models.TextField(blank=True, help_text="Des noms alternatifs")),
                ("definition_short", models.CharField(help_text="La definition succinte du mot", max_length=150)),
                ("description", models.TextField(blank=True, help_text="Une description longue du mot")),
                (
                    "description_accessible_url",
                    models.URLField(blank=True, help_text="Un lien pour aller plus loin", max_length=500),
                ),
                ("added", models.DateField(blank=True, help_text="La date d'ajout du mot", null=True)),
                ("created", models.DateField(auto_now_add=True, help_text="La date de création du mot")),
                ("updated", models.DateField(auto_now=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
    ]