from django.core.management import BaseCommand

from api.models import Question


class Command(BaseCommand):
    """
    Usage:
    python manage.py reset_question_stats <question_id>
    python manage.py reset_question_stats <question_id> --no-input (to skip input, e.g. for tests)
    """

    help = """Clean a question's stats"""

    def add_arguments(self, parser):
        parser.add_argument(
            "question_id", type=int, help="Indicates the id of the question"
        )
        parser.add_argument(
            "--no-input",
            default=False,
            action="store_true",
            dest="no-input",
            help="Skip user input",
        )

    def handle(self, *args, **options):
        question_id = options["question_id"]
        question = Question.objects.get(pk=question_id)

        print("=== reset_question_stats on Question", question)
        print(question.__dict__)

        # question aggregated stats
        print("=== aggregated stats (QuestionAggStat)")
        print("- answer_count:", question.agg_stats.answer_count)
        print("- answer_success_count:", question.agg_stats.answer_success_count)
        print("- like_count: was", question.agg_stats.like_count)
        print("- dislike_count: was", question.agg_stats.dislike_count)

        # question answer events : QuestionAnswerEvent & QuestionFeedbackEvent
        print(
            "=== answer & feedbacks stats (QuestionAnswerEvent & QuestionFeedbackEvent)"
        )
        question_event_stats = question.stats
        print("- question answer stats: found", question_event_stats.count())
        question_event_feedbacks = question.feedbacks
        print("- question feedbacks: found", question_event_feedbacks.count())

        # user input
        if options.get("no-input"):
            answer = "Y"
        else:
            answer = input("Are you sure you want to reset these stats ? (Y/n)")

        # reset stats
        if answer == "Y":
            print("=== resetting stats...")
            question.agg_stats.answer_count = 0
            question.agg_stats.answer_success_count = 0
            question.agg_stats.like_count = 0
            question.agg_stats.dislike_count = 0
            question.agg_stats.save()

            question_event_stats.all().delete()
            question_event_feedbacks.all().delete()

            print("=== reset_question_stats done")
