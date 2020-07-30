QUESTION_TYPE_QCM = "QCM"
QUESTION_TYPE_QCM_RM = "QCM-RM"
QUESTION_TYPE_VF = "VF"
QUESTION_TYPE_CHOICES = [
    (QUESTION_TYPE_QCM, "Questionnaire à choix multiples"),
    (QUESTION_TYPE_QCM_RM, "Questionnaire à choix multiples avec réponses multiples"),
    (QUESTION_TYPE_VF, "Vrai ou Faux"),
]
QUESTION_TYPE_CHOICE_LIST = [c[0] for c in QUESTION_TYPE_CHOICES]

QUESTION_VALIDATION_STATUS_NEW = "Brouillon"
QUESTION_VALIDATION_STATUS_IN_PROGRESS = "A valider"
QUESTION_VALIDATION_STATUS_OK = "Validée"
QUESTION_VALIDATION_STATUS_REMOVED = "Écartée"
QUESTION_VALIDATION_STATUS_LIST = [
    QUESTION_VALIDATION_STATUS_NEW,
    QUESTION_VALIDATION_STATUS_IN_PROGRESS,
    QUESTION_VALIDATION_STATUS_OK,
    QUESTION_VALIDATION_STATUS_REMOVED,
]

QUESTION_DIFFICULTY_EASY = 1
QUESTION_DIFFICULTY_CHOICES = [
    (0, "Junior"),
    (QUESTION_DIFFICULTY_EASY, "Facile"),
    (2, "Moyen"),
    (3, "Difficile"),
    (4, "Expert"),
]
QUESTION_DIFFICULTY_CHOICE_LIST = [c[0] for c in QUESTION_DIFFICULTY_CHOICES]

QUESTION_ANSWER_CHOICE_LIST = ["a", "b", "c", "d"]

FEEDBACK_LIKE = "like"
FEEDBACK_DISLIKE = "dislike"
FEEDBACK_CHOICES = [
    (FEEDBACK_LIKE, "Positif"),
    (FEEDBACK_DISLIKE, "Négatif"),
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
    # "quiz_answer_count",
    "question_feedback_count",
    # "quiz_feedback_count",
]
AGGREGATION_QUIZ_FIELD_CHOICE_LIST = ["quiz_answer_count", "quiz_feedback_count"]
AGGREGATION_SCALE_CHOICE_LIST = ["day", "week", "month"]
AGGREGATION_SINCE_CHOICE_LIST = ["total", "month", "week"]

CONTRIBUTION_TYPE_LIST = [
    "nouvelle question",
    "commentaire application",
    "commentaire question",
    "commentaire quiz",
]


def daily_stat_hour_split_jsonfield_default_value():
    return DEFAULT_DAILY_STAT_HOUR_SPLIT
