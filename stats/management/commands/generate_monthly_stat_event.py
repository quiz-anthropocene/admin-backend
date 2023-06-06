from datetime import timedelta

from django.core.management import BaseCommand
from django.utils import timezone

from activity.utilities import create_event
from contributions.models import Comment
from stats.models import DailyStat


class Command(BaseCommand):
    """
    Command to generate an event with the monthly stats
    By default, it will compute on the last month (run ideally on the first day of the next month :)

    Usage:
    python manage.py generate_monthly_stat_event
    """

    def handle(self, *args, **kwargs):
        print("=== generate_monthly_stat_event running")
        weekday = timezone.now() - timedelta(days=25)  # last month
        weekday_year = weekday.year
        weekday_month = weekday.month

        question_answer_count_month = DailyStat.objects.agg_count(
            "question_answer_count", since="month", week_or_month_iso_number=weekday_month, year=weekday_year
        )
        quiz_answer_count_month = DailyStat.objects.agg_count(
            "quiz_answer_count", since="month", week_or_month_iso_number=weekday_month, year=weekday_year
        )
        question_feedback_count_month = DailyStat.objects.agg_count(
            "question_feedback_count", since="month", week_or_month_iso_number=weekday_month, year=weekday_year
        )
        quiz_feedback_count_month = DailyStat.objects.agg_count(
            "quiz_feedback_count", since="month", week_or_month_iso_number=weekday_month, year=weekday_year
        )
        comment_count_month = Comment.objects.exclude_contributor_work().count()

        extra_data = {
            "event_object_type": "MONTHLY_AGG_STAT",
            "type": "last_month",
            "month": weekday_month,
            "year": weekday_year,
            "question_answer_count": question_answer_count_month,
            "quiz_answer_count": quiz_answer_count_month,
            "question_feedback_count": question_feedback_count_month,
            "quiz_feedback_count": quiz_feedback_count_month,
            "comment_count": comment_count_month,
        }

        create_event(user=None, event_verb="COMPUTED", extra_data=extra_data)
        print("Done !")
