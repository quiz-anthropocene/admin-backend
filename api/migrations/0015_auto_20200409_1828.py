# Generated by Django 3.0.4 on 2020-04-09 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_rename_question_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='has_ordered_answers',
            field=models.BooleanField(default=True, help_text='Les choix de réponse sont dans un ordre figé, et ne doivent pas être mélangés'),
        ),
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.ForeignKey(help_text='Une seule catégorie possible', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='questions', to='api.QuestionCategory'),
        ),
    ]
