# Generated by Django 3.1.4 on 2021-02-17 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0076_question_answer_reading_recommendation"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(
                    model_name="questionanswerevent", name="question",
                ),
                migrations.RemoveField(
                    model_name="questionfeedbackevent", name="question",
                ),
                migrations.RemoveField(model_name="quizanswerevent", name="quiz",),
                migrations.RemoveField(model_name="quizfeedbackevent", name="quiz",),
            ],
            # reusing the table, don't drop it
            database_operations=[],
        ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(name="DailyStat",),
                migrations.DeleteModel(name="QuestionAggStat",),
                migrations.DeleteModel(name="QuestionAnswerEvent",),
                migrations.DeleteModel(name="QuestionFeedbackEvent",),
                migrations.DeleteModel(name="QuizAnswerEvent",),
                migrations.DeleteModel(name="QuizFeedbackEvent",),
            ],
            # want to reuse the table, don't drop it
            database_operations=[
                migrations.AlterModelTable(name="DailyStat", table="stats_dailystat",),
                migrations.AlterModelTable(
                    name="QuestionAggStat", table="stats_questionaggstat",
                ),
                migrations.AlterModelTable(
                    name="QuestionAnswerEvent", table="stats_questionanswerevent",
                ),
                migrations.AlterModelTable(
                    name="QuestionFeedbackEvent", table="stats_questionfeedbackevent",
                ),
                migrations.AlterModelTable(
                    name="QuizAnswerEvent", table="stats_quizanswerevent",
                ),
                migrations.AlterModelTable(
                    name="QuizFeedbackEvent", table="stats_quizfeedbackevent",
                ),
            ],
        ),
    ]
