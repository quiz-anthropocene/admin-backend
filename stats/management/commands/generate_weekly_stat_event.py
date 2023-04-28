from django.core.management import BaseCommand
from django.utils import timezone

from activity.utilities import create_event
from stats.models import DailyStat


class Command(BaseCommand):
    """
    Usage:
    python manage.py generate_weekly_stat_event
    """

    def handle(self, *args, **kwargs):
        now = timezone.now()
        now_year = now.year
        # now_month = now.month
        now_week = now.isocalendar().week

        question_answer_count_last_week = DailyStat.objects.agg_count(
            "question_answer_count", since="week", week_or_month_iso_number=(now_week - 1), year=now_year
        )
        print(question_answer_count_last_week)
        quiz_answer_count_last_week = DailyStat.objects.agg_count(
            "quiz_answer_count", since="week", week_or_month_iso_number=(now_week - 1), year=now_year
        )
        print(quiz_answer_count_last_week)

        create_event(event_user=None, event_verb=None)
