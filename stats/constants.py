from django.utils.translation import gettext_lazy as _


FEEDBACK_LIKE = "like"
FEEDBACK_DISLIKE = "dislike"
FEEDBACK_CHOICES = [
    (FEEDBACK_LIKE, _("Positive")),
    (FEEDBACK_DISLIKE, _("Negative")),
]

QUESTION_SOURCE_QUESTION = "question"
QUESTION_SOURCE_QUIZ = "quiz"
QUESTION_SOURCE_CHOICES = [
    (QUESTION_SOURCE_QUESTION, "Question"),
    (QUESTION_SOURCE_QUIZ, "Quiz"),
]

DEFAULT_DAILY_STAT_HOUR_SPLIT = {
    str(h): {
        "question_answer_count": 0,
        "question_answer_from_quiz_count": 0,
        "quiz_answer_count": 0,
        "question_feedback_count": 0,
        "question_feedback_from_quiz_count": 0,
        "quiz_feedback_count": 0,
    }
    for h in range(24)  # '0' à '23'
}

AGGREGATION_FIELD_CHOICE_LIST = [
    "question_answer_count",
    "quiz_answer_count",
    "question_feedback_count",
    # "quiz_feedback_count",
]
AGGREGATION_QUIZ_FIELD_CHOICE_LIST = ["quiz_answer_count", "quiz_feedback_count"]
AGGREGATION_SCALE_CHOICE_LIST = ["day", "week", "month"]
AGGREGATION_SINCE_CHOICE_LIST = ["total", "last_30_days", "month", "week"]
AGGREGATION_SINCE_DATE_DEFAULT = "2020-01-01"


def daily_stat_hour_split_jsonfield_default_value():
    return DEFAULT_DAILY_STAT_HOUR_SPLIT
