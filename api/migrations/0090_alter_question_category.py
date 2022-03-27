# Generated by Django 4.0.3 on 2022-03-24 23:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("categories", "0001_initial"),
        ("api", "0089_migrate_category_model"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="category",
            field=models.ForeignKey(
                blank=True,
                help_text="Une seule catégorie possible",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="questions",
                to="categories.category",
            ),
        ),
    ]