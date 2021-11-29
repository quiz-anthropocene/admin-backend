# Generated by Django 3.2.9 on 2021-11-29 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='notion_questions_scope_0_last_imported',
            field=models.DateTimeField(blank=True, editable=False, help_text='La dernière fois que les questions ont été importées depuis Notion', null=True),
        ),
    ]
