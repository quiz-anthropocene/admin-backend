from datetime import timedelta

from django.core.management import BaseCommand
from django.utils import timezone

from activity.utilities import create_event
from contributions.models import Comment
from stats.models import DailyStat


class Command(BaseCommand):
    """
    Command to generate an event with the weekly stats
    By default, it will compute on the last (complete) week (run ideally on a Monday :)

    Usage:
    python manage.py generate_weekly_stat_event
    """

    def handle(self, *args, **kwargs):
        print("=== generate_weekly_stat_event running")
        weekday = timezone.now() - timedelta(days=7)  # last week
        weekday_year = weekday.year
        weekday_week = weekday.isocalendar().week

        question_answer_count_week = DailyStat.objects.agg_count(
            "question_answer_count", since="week", week_or_month_iso_number=weekday_week, year=weekday_year
        )
        quiz_answer_count_week = DailyStat.objects.agg_count(
            "quiz_answer_count", since="week", week_or_month_iso_number=weekday_week, year=weekday_year
        )
        question_feedback_count_week = DailyStat.objects.agg_count(
            "question_feedback_count", since="week", week_or_month_iso_number=weekday_week, year=weekday_year
        )
        quiz_feedback_count_week = DailyStat.objects.agg_count(
            "quiz_feedback_count", since="week", week_or_month_iso_number=weekday_week, year=weekday_year
        )
        comment_count_week = (
            Comment.objects.exclude_contributor_work()
            .filter(created__week=weekday_week)
            .filter(created__year=weekday_year)
            .count()
        )

        extra_data = {
            "event_object_type": "WEEKLY_AGG_STAT",
            "type": "last_week",
            "week": weekday_week,
            "year": weekday_year,
            "question_answer_count": question_answer_count_week,
            "quiz_answer_count": quiz_answer_count_week,
            "question_feedback_count": question_feedback_count_week,
            "quiz_feedback_count": quiz_feedback_count_week,
            "comment_count": comment_count_week,
        }

        create_event(user=None, event_verb="COMPUTED", extra_data=extra_data)
        print("Done !")
