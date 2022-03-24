from django.core.management import BaseCommand

from api.models import Question  # , QuestionAggStat


def print_question_stats(question):
    print("===", question)
    # print(question.__dict__)

    # question stats
    print("> basic stats")
    print("- answer_count:", question.answer_count)
    print("- answer_success_count:", question.answer_success_count)
    print("- like_count: was", question.like_count)
    print("- dislike_count: was", question.dislike_count)

    # question answer events : QuestionAnswerEvent
    print("> answer stats & feedbacks")
    question_event_stats = question.stats
    print("- answer stats: found", question_event_stats.count())

    question_event_feedbacks = question.feedbacks
    print("- question feedbacks: found", question_event_feedbacks.count())


# def reset_question_stats(question):
#     question.answer_count = 0
#     question.answer_success_count = 0
#     question.like_count = 0
#     question.dislike_count = 0
#     question.save()

#     question_event_stats.all().delete()
#     question_event_feedbacks.all().delete()

#     print("Done")


class Command(BaseCommand):
    """
    Usage:
    python manage.py init_question_agg_stats
    python manage.py init_question_agg_stats --id <question_id>
    """

    help = """Initialize question agg stats"""

    def add_arguments(self, parser):
        parser.add_argument("--id", action="append", type=int, help="Indicates the id of the question")

    def handle(self, *args, **options):
        if options.get("id"):
            question_id = options.get("id")[0]
            questions = Question.objects.filter(pk=question_id)
        else:
            questions = Question.objects.all()

        for question in questions:
            # print stats
            print_question_stats(question)

            # # reset stats
            # answer = input("Are you sure you want to reset these stats ? (Y/n)")
            # if answer == "Y":
            #     reset_question_stats(question)
