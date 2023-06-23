from datetime import timedelta

from django.core.management import BaseCommand
from django.utils import timezone

from stats.models import QuestionAnswerEvent, QuizAnswerEvent
from users.models import User


class Command(BaseCommand):
    """
    Command to send an e-mail to each contributor with its monthly stats
    By default, it will compute on the last month (run ideally on the first day of the next month :)

    Usage:
    python manage.py send_contributor_monthly_recap_email --dry-run
    python manage.py send_contributor_monthly_recap_email
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run", dest="dry_run", action="store_true", help="Dry run (no sends nor changes to the DB)"
        )

    def handle(self, *args, **options):
        print("=== send_contributor_monthly_recap_email running")
        weekday = timezone.now() - timedelta(days=25)  # last month
        weekday_year = weekday.year
        weekday_month = weekday.month

        contributors = User.objects.all_contributors()
        print(f"{contributors.count()} contributors")
        contributors_with_public_content = contributors.has_public_content()
        print(f"{contributors_with_public_content.count()} contributors with public content")

        for user in contributors_with_public_content:
            question_answer_count_month = QuestionAnswerEvent.objects.filter(
                question__in=user.questions.public().validated()
            ).agg_count(since="month", week_or_month_iso_number=weekday_month, year=weekday_year)
            quiz_answer_count_month = QuizAnswerEvent.objects.filter(
                quiz__in=user.quizs.public().published()
            ).agg_count(since="month", week_or_month_iso_number=weekday_month, year=weekday_year)

            parameters = {
                "QUESTION_PUBLIC_VALIDATED_COUNT": user.question_public_validated_count,
                "QUIZ_PUBLIC_PUBLISHED_COUNT": user.quiz_public_published_count,
                "QUESTION_ANSWER_COUNT_MONTH": question_answer_count_month,
                "QUIZ_ANSWER_COUNT_MONTH": quiz_answer_count_month,
                # "COMMENT_COUNT_MONTH": 0
            }

            if not options["dry_run"]:
                print("user")
                print(parameters)
                # send email
                # log metadata
