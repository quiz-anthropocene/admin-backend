from django.core.management import BaseCommand

from api.models import Quiz


class Command(BaseCommand):
    """
    Usage:
    - python manage.py sanitize_quiz_question_ordering
    - python manage.py sanitize_quiz_question_ordering --fix
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--fix",
            default=False,
            action="store_true",
            dest="fix",
            help="Fix ordering errors",
        )

    def handle(self, *args, **kwargs):
        for quiz in Quiz.objects.all():
            print("-----", quiz.id, quiz.name)
            for index, qq in enumerate(quiz.quizquestion_set.all()):
                order_correct = qq.order == index + 1
                if not order_correct:
                    print(
                        f"question {qq.question.id} /",
                        f"current order: {qq.order} /",
                        f"correct order: {index + 1}",
                    )
                    if kwargs.get("fix"):
                        qq.order = index + 1
                        qq.save()
                        print("... fixed")
