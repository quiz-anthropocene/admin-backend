from django.core.management import BaseCommand

from api.models import Quiz


class Command(BaseCommand):
    """
    Usage:
    python manage.py reset_quiz_stats <quiz_id>
    python manage.py reset_quiz_stats <quiz_id> --no-input (to skip input, e.g. for tests)
    """

    help = """Clean a quiz's stats"""

    def add_arguments(self, parser):
        parser.add_argument("quiz_id", type=int, help="Indicates the id of the quiz")
        parser.add_argument(
            "--no-input",
            default=False,
            action="store_true",
            dest="no-input",
            help="Skip user input",
        )

    def handle(self, *args, **options):
        quiz_id = options["quiz_id"]
        quiz = Quiz.objects.get(pk=quiz_id)

        print("=== reset_quiz_stats on Quiz", quiz)
        print(quiz.__dict__)

        # quiz aggregated stats
        print("=== quiz don't have aggregated stats")

        # quiz answer events : QuizAnswerEvent & QuizFeedbackEvent
        print("=== latest answer & feedbacks stats (QuizAnswerEvent & QuizFeedbackEvent)")
        quiz_event_stats = quiz.stats
        print("- quiz answer stats: found", quiz_event_stats.count())
        quiz_event_feedbacks = quiz.feedbacks
        print("- quiz feedbacks: found", quiz_event_feedbacks.count())

        # user input
        if options.get("no-input"):
            answer = "Y"
        else:
            answer = input("Are you sure you want to reset these stats ? (Y/n)")

        # reset stats
        if answer == "Y":
            print("=== resetting stats...")
            quiz_event_stats.all().delete()
            quiz_event_feedbacks.all().delete()

            print("=== reset_quiz_stats done")
