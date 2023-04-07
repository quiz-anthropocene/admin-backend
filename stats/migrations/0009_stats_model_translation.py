# Generated by Django 4.1.5 on 2023-03-12 17:55

import django.utils.timezone
from django.db import migrations, models

import stats.constants


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0008_alter_linkclickevent_question_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dailystat",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name="Creation date"),
        ),
        migrations.AlterField(
            model_name="dailystat",
            name="date",
            field=models.DateField(help_text="Date of statistics"),
        ),
        migrations.AlterField(
            model_name="dailystat",
            name="hour_split",
            field=models.JSONField(
                default=stats.constants.daily_stat_hour_split_jsonfield_default_value, help_text="Hourly statistics"
            ),
        ),
        migrations.AlterField(
            model_name="dailystat",
            name="question_answer_count",
            field=models.PositiveIntegerField(default=0, help_text="Question answer count"),
        ),
        migrations.AlterField(
            model_name="dailystat",
            name="question_answer_from_quiz_count",
            field=models.PositiveIntegerField(default=0, help_text="Question within quiz answer count"),
        ),
        migrations.AlterField(
            model_name="dailystat",
            name="question_feedback_count",
            field=models.PositiveIntegerField(default=0, help_text="Question feedback count"),
        ),
        migrations.AlterField(
            model_name="dailystat",
            name="question_feedback_from_quiz_count",
            field=models.PositiveIntegerField(default=0, help_text="Question within quiz feedback count"),
        ),
        migrations.AlterField(
            model_name="dailystat",
            name="question_public_answer_count",
            field=models.PositiveIntegerField(default=0, help_text="Public question answer count"),
        ),
        migrations.AlterField(
            model_name="dailystat",
            name="quiz_answer_count",
            field=models.PositiveIntegerField(default=0, help_text="Quiz answer count"),
        ),
        migrations.AlterField(
            model_name="dailystat",
            name="quiz_feedback_count",
            field=models.PositiveIntegerField(default=0, help_text="Quiz feedback count"),
        ),
        migrations.AlterField(
            model_name="dailystat",
            name="quiz_public_answer_count",
            field=models.PositiveIntegerField(default=0, help_text="Public quiz answer count"),
        ),
        migrations.AlterField(
            model_name="dailystat",
            name="updated",
            field=models.DateField(auto_now=True, verbose_name="Last update date"),
        ),
        migrations.AlterField(
            model_name="linkclickevent",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name="Creation date"),
        ),
        migrations.AlterField(
            model_name="linkclickevent",
            name="field_name",
            field=models.CharField(blank=True, max_length=50, verbose_name="Field name"),
        ),
        migrations.AlterField(
            model_name="linkclickevent",
            name="link_url",
            field=models.URLField(blank=True, max_length=500, verbose_name="Clicked link"),
        ),
        migrations.AlterField(
            model_name="questionaggstat",
            name="answer_count",
            field=models.PositiveIntegerField(default=0, help_text="Answer count"),
        ),
        migrations.AlterField(
            model_name="questionaggstat",
            name="answer_success_count",
            field=models.PositiveIntegerField(default=0, help_text="Right answer count"),
        ),
        migrations.AlterField(
            model_name="questionaggstat",
            name="dislike_count",
            field=models.PositiveIntegerField(default=0, help_text="Dislike count"),
        ),
        migrations.AlterField(
            model_name="questionaggstat",
            name="like_count",
            field=models.PositiveIntegerField(default=0, help_text="Like count"),
        ),
        migrations.AlterField(
            model_name="questionanswerevent",
            name="choice",
            field=models.CharField(
                choices=[
                    ("a", "a"),
                    ("b", "b"),
                    ("c", "c"),
                    ("d", "d"),
                    ("ab", "ab"),
                    ("ac", "ac"),
                    ("ad", "ad"),
                    ("bc", "bc"),
                    ("bd", "bd"),
                    ("cd", "cd"),
                    ("abc", "abc"),
                    ("abd", "abd"),
                    ("acd", "acd"),
                    ("bcd", "bcd"),
                    ("abcd", "abcd"),
                ],
                help_text="Answer chosen by the user",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="questionanswerevent",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name="Creation date"),
        ),
        migrations.AlterField(
            model_name="questionanswerevent",
            name="source",
            field=models.CharField(
                choices=[("question", "Question"), ("quiz", "Quiz")],
                default="question",
                help_text="Context in which the question was answered",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="questionfeedbackevent",
            name="choice",
            field=models.CharField(
                choices=[("like", "Positive"), ("dislike", "Negative")],
                default="like",
                help_text="Feedback left on the question",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="questionfeedbackevent",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name="Creation date"),
        ),
        migrations.AlterField(
            model_name="questionfeedbackevent",
            name="source",
            field=models.CharField(
                choices=[("question", "Question"), ("quiz", "Quiz")],
                default="question",
                help_text="Context in which the feedback was left",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="quizaggstat",
            name="answer_count",
            field=models.PositiveIntegerField(default=0, help_text="Answer count"),
        ),
        migrations.AlterField(
            model_name="quizaggstat",
            name="dislike_count",
            field=models.PositiveIntegerField(default=0, help_text="Dislike count"),
        ),
        migrations.AlterField(
            model_name="quizaggstat",
            name="like_count",
            field=models.PositiveIntegerField(default=0, help_text="Like count"),
        ),
        migrations.AlterField(
            model_name="quizanswerevent",
            name="answer_success_count",
            field=models.IntegerField(default=0, help_text="Right answer count"),
        ),
        migrations.AlterField(
            model_name="quizanswerevent",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name="Creation date"),
        ),
        migrations.AlterField(
            model_name="quizanswerevent",
            name="duration_seconds",
            field=models.IntegerField(default=0, help_text="Duration (in seconds) to complete the quiz"),
        ),
        migrations.AlterField(
            model_name="quizanswerevent",
            name="question_answer_split",
            field=models.JSONField(default=dict, help_text="Details per question"),
        ),
        migrations.AlterField(
            model_name="quizanswerevent",
            name="question_count",
            field=models.IntegerField(default=0, help_text="Quiz question count"),
        ),
        migrations.AlterField(
            model_name="quizfeedbackevent",
            name="choice",
            field=models.CharField(
                choices=[("like", "Positive"), ("dislike", "Negative")],
                default="like",
                help_text="Feedback left on the quiz",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="quizfeedbackevent",
            name="created",
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name="Creation date"),
        ),
    ]