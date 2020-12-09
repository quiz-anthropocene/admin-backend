# from datetime import date, timedelta

from django.db.models import Count, F

from api.models import (
    Category,
    Tag,
    Question,
    Quiz,
    QuizAnswerEvent,
    QuizFeedbackEvent,
    Contribution,
    DailyStat,
)


def category_stats():
    category_count = Category.objects.count()

    return {"category_count": category_count}


def tag_stats():
    tag_count = Tag.objects.count()

    return {"tag_count": tag_count}


def question_stats():
    question_count = Question.objects.count()
    question_per_validation_status_count = (
        Question.objects.all()
        .values("validation_status")
        .annotate(total=Count("validation_status"))
        .order_by("-total")
    )

    return {
        "question_count": question_count,
        "question_per_validation_status_count": list(
            question_per_validation_status_count
        ),
    }


def quiz_stats():
    quiz_count = Quiz.objects.count()
    quiz_per_publish_count = (
        Quiz.objects.all()
        .values("publish")
        .annotate(total=Count("publish"))
        .order_by("-total")
    )

    return {
        "quiz_count": quiz_count,
        "quiz_per_publish_count": list(quiz_per_publish_count),
    }


def answer_stats():
    # total question/quiz answer/feedback count
    question_answer_count = DailyStat.objects.agg_count("question_answer_count")
    quiz_answer_count = QuizAnswerEvent.objects.count()
    # last 30 days
    question_answer_count_last_30_days = DailyStat.objects.agg_count(
        "question_answer_count", since="last_30_days"
    )
    quiz_answer_count_last_30_days = QuizAnswerEvent.objects.last_30_days().count()
    # # current month
    # current_month_iso_number = date.today().month
    # question_answer_count_current_month = QuestionAnswerEvent.objects.filter(
    #     created__date__month=current_month_iso_number
    # ).count() + DailyStat.objects.agg_count(
    #     "question_answer_count",
    #     since="month",
    #     week_or_month_iso_number=current_month_iso_number,
    # )
    # quiz_answer_count_current_month = QuizAnswerEvent.objects.filter(
    #     created__date__month=current_month_iso_number
    # ).count() + DailyStat.objects.agg_count(
    #     "quiz_answer_count",
    #     since="month",
    #     week_or_month_iso_number=current_month_iso_number,
    # )
    # # current week
    # current_week_iso_number = date.today().isocalendar()[1]
    # question_answer_count_current_week = QuestionAnswerEvent.objects.filter(
    #     created__date__week=current_week_iso_number
    # ).count() + DailyStat.objects.agg_count(
    #     "question_answer_count",
    #     since="week",
    #     week_or_month_iso_number=current_week_iso_number,
    # )
    # quiz_answer_count_current_week = QuizAnswerEvent.objects.filter(
    #     created__date__week=current_week_iso_number
    # ).count() + DailyStat.objects.agg_count(
    #     "quiz_answer_count",
    #     since="week",
    #     week_or_month_iso_number=current_week_iso_number,
    # )

    return {
        # "total": {
        "question_answer_count": question_answer_count,
        "quiz_answer_count": quiz_answer_count,
        # last 30 days
        "question_answer_count_last_30_days": question_answer_count_last_30_days,
        "quiz_answer_count_last_30_days": quiz_answer_count_last_30_days,
        # },
        # "current_month": {
        #     "month_iso_number": current_month_iso_number,
        #     "question_answer_count": question_answer_count_current_month,
        #     "quiz_answer_count": quiz_answer_count_current_month,
        # },
        # "current_week": {
        #     "week_iso_number": current_week_iso_number,
        #     "question_answer_count": question_answer_count_current_week,
        #     "quiz_answer_count": quiz_answer_count_current_week,
        # },
    }


def contribution_stats():
    question_feedback_count = DailyStat.objects.agg_count("question_feedback_count")
    quiz_feedback_count = QuizFeedbackEvent.objects.count()
    contribution_count = Contribution.objects.count()

    return {
        "question_feedback_count": question_feedback_count,
        "quiz_feedback_count": quiz_feedback_count,
        "contribution_count": contribution_count,
    }


def author_aggregate():
    question_authors = list(
        Question.objects.validated()
        .values(name=F("author"))
        .annotate(question_count=Count("author"))
        .order_by("name")
    )
    quiz_authors = list(
        Quiz.objects.published()
        .values("author")  # cannot use name= (already a field in Quiz model)
        .annotate(quiz_count=Count("author"))
        .order_by("author")
    )
    # merge known quiz_authors into question_authors
    question_quiz_authors = []
    for question_author in question_authors:
        question_author["quiz_count"] = next(
            (
                quiz_author["quiz_count"]
                for quiz_author in quiz_authors
                if question_author["name"] == quiz_author["author"]
            ),
            0,
        )
        question_quiz_authors.append(question_author)
    # manage new quiz_authors
    question_authors_flat = [
        question_author["name"] for question_author in question_authors
    ]
    new_quiz_authors = [
        quiz_author
        for quiz_author in quiz_authors
        if quiz_author["author"] not in question_authors_flat
    ]
    if len(new_quiz_authors):
        for new_quiz_author in new_quiz_authors:
            question_quiz_authors.append(
                {
                    "name": new_quiz_author["author"],
                    "question_count": 0,
                    "quiz_count": new_quiz_author["quiz_count"],
                }
            )
        # sort
        question_quiz_authors = sorted(question_quiz_authors, key=lambda k: k["name"])

    return question_quiz_authors
