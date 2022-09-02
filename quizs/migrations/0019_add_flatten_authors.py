import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quizs", "0018_quizauthors_quiz_authors_alter_quiz_author_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="quiz",
            name="authors_list",
            field=models.CharField(blank=True, max_length=300, verbose_name="Auteurs"),
        ),
        migrations.AddField(
            model_name="quiz",
            name="authors_id_list",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.PositiveIntegerField(),
                blank=True,
                default=list,
                size=None,
                verbose_name="Auteurs_ID",
            ),
        ),
    ]
