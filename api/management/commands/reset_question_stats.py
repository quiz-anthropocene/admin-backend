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
        print(question)

        # Reset question stats
        print("Reset question stats")
        print("- answer_count: was", question.answer_count, "--> now 0")
        question.answer_count = 0
        print("- answer_success_count: was", question.answer_success_count, "--> now 0")
        question.answer_success_count = 0
        print("- like_count: was", question.like_count, "--> now 0")
        question.like_count = 0
        print("- dislike_count: was", question.dislike_count, "--> now 0")
        question.dislike_count = 0
        question.save()

        # Reset question answer events : QuestionAnswerEvent
        print("Reset question answer stats & feedbacks")
        question_event_stats = question.stats
        print("- answer stats: found", question_event_stats.count(), "--> now 0")
        question_event_stats.all().delete()
        question_event_feedbacks = question.feedbacks
        print(
            "- question feedbacks: found", question_event_feedbacks.count(), "--> now 0"
        )
        question_event_feedbacks.all().delete()

        print("Done")
