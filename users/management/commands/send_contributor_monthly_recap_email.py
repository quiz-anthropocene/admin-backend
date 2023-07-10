from datetime import timedelta

from django.conf import settings
from django.core.management import BaseCommand
from django.utils import timezone

from contributions.models import Comment
from core.utils.sendinblue import send_transactional_email_with_template_id
from stats.models import QuizAnswerEvent
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
        # for now we contact only contributors with a public_quiz
        contributors_with_public_quiz = contributors.has_public_quiz()  # has_public_content()
        print(f"{contributors_with_public_quiz.count()} contributors with public quiz")

        for user in contributors_with_public_quiz:
            # quiz stats
            quiz_public_published = user.quizs.public().published()
            quiz_public_published_count = quiz_public_published.count()
            quiz_answer_count_month = QuizAnswerEvent.objects.filter(quiz__in=quiz_public_published).agg_count(
                since="month", week_or_month_iso_number=weekday_month, year=weekday_year
            )
            quiz_public_published_string = (
                f"ton quiz {quiz_public_published.first().name}"
                if (quiz_public_published_count == 1)
                else f"tes {quiz_public_published_count} quizs"
            )
            # question stats
            question_public_validated = user.questions.public().validated()
            # question_public_validated_count = question_public_validated.count()
            # quiz_answer_count_month = QuestionAnswerEvent.objects.filter(
            #     question__in=user.questions.public().validated()
            # ).agg_count(since="month", week_or_month_iso_number=weekday_month, year=weekday_year)
            # comment stats
            quiz_comment_count_month = (
                Comment.objects.exclude_contributor_work()
                .filter(quiz__in=quiz_public_published)
                .agg_count(since="month", week_or_month_iso_number=weekday_month, year=weekday_year)
            )
            question_comment_count_month = (
                Comment.objects.exclude_contributor_work()
                .filter(question__in=question_public_validated)
                .agg_count(since="month", week_or_month_iso_number=weekday_month, year=weekday_year)
            )

            parameters = {
                "firstName": user.first_name,
                "lastMonth": weekday.strftime("%B %Y"),
                "quizAnswerCountLastMonth": quiz_answer_count_month,
                "quizCountString": quiz_public_published_string,
                "commentCountLastMonth": quiz_comment_count_month + question_comment_count_month,
            }

            if not options["dry_run"]:
                # send email
                send_transactional_email_with_template_id(
                    to_email=user.email,
                    to_name=user.full_name,
                    template_id=int(settings.SIB_CONTRIBUTOR_MONTHLY_RECAP_TEMPLATE_ID),
                    parameters=parameters,
                )

                # log email
                log_item = {
                    "action": f"email_contributor_monthly_recap_{weekday_year}_{weekday_month}",
                    "email_to": user.email,
                    # "email_subject": email_subject,
                    # "email_body": email_body,
                    "email_timestamp": timezone.now().isoformat(),
                    "metadata": {"parameters": parameters},
                }
                user.logs.append(log_item)
                user.save()
