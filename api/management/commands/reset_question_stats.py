from django.core.management import BaseCommand

from api.models import Question


class Command(BaseCommand):
    """
    Usage:
    python manage.py reset_question_stats <question_id>
    """

    help = """Clean a question's stats"""

    def add_arguments(self, parser):
        parser.add_argument(
            "question_id", type=int, help="Indicates the id of the question"
        )

    def handle(self, *args, **options):
        question_id = options["question_id"]
        question = Question.objects.get(pk=question_id)

        print("===", question)
        print(question.__dict__)

        # question stats
        print("=== basic stats (QuestionAggStat)")
        print("- answer_count:", question.agg_stats.answer_count)
        print("- answer_success_count:", question.agg_stats.answer_success_count)
        print("- like_count: was", question.agg_stats.like_count)
        print("- dislike_count: was", question.agg_stats.dislike_count)

        # question answer events : QuestionAnswerEvent
        print("=== answer stats & feedbacks (QuestionAnswerEvent)")
        question_event_stats = question.stats
        print("- answer stats: found", question_event_stats.count())
        question_event_feedbacks = question.feedbacks
        print("- question feedbacks: found", question_event_feedbacks.count())

        # reset stats
        answer = input("Are you sure you want to reset these stats ? (Y/n)")
        if answer == "Y":
            question.agg_stats.answer_count = 0
            question.agg_stats.answer_success_count = 0
            question.agg_stats.like_count = 0
            question.agg_stats.dislike_count = 0
            question.agg_stats.save()

            question_event_stats.all().delete()
            question_event_feedbacks.all().delete()

            print("Done")
