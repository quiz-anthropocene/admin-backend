QUESTION_TYPE_CHOICES = [
    ("QCM", "Questionnaire à choix multiples (QCM)"),
    ("VF", "Vrai ou Faux"),
]

QUESTION_VALIDATION_STATUS_NEW = "Nouvelle question"
QUESTION_VALIDATION_STATUS_IN_PROGRESS = "En cours de validation"
QUESTION_VALIDATION_STATUS_OK = "Validée"
QUESTION_VALIDATION_STATUS_REMOVED = "Écartée"
QUESTION_VALIDATION_STATUS_LIST = [
    QUESTION_VALIDATION_STATUS_NEW,
    QUESTION_VALIDATION_STATUS_IN_PROGRESS,
    QUESTION_VALIDATION_STATUS_OK,
    QUESTION_VALIDATION_STATUS_REMOVED,
]

# QUESTION_CATEGORY_CHOICES = [
#     ("biodiversité", "Biodiversité"),
#     ("climat", "Climat"),
#     ("consommation", "Consommation, Leviers d'action"),
#     ("énergie", "Energie"),
#     ("histoire", "Histoire, Anthropologie, Politique, Démographie"),
#     ("pollution", "Pollution"),
#     ("ressources", "Ressources (hors énergie)"),
#     ("autre", "Autre"),
# ]

QUESTION_DIFFICULTY_EASY = 1
QUESTION_DIFFICULTY_CHOICES = [
    (0, "Junior"),
    (QUESTION_DIFFICULTY_EASY, "Facile"),
    (2, "Moyen"),
    (3, "Difficile"),
    (4, "Expert"),
]

QUESTION_FEEDBACK_LIKE = "like"
QUESTION_FEEDBACK_DISLIKE = "dislike"
QUESTION_FEEDBACK_CHOICES = [
    (QUESTION_FEEDBACK_LIKE, "Positif"),
    (QUESTION_FEEDBACK_DISLIKE, "Négatif"),
]

QUESTION_SOURCE_QUESTION = "question"
QUESTION_SOURCE_QUIZ = "quiz"
QUESTION_SOURCE_CHOICES = [
    (QUESTION_SOURCE_QUESTION, "Question"),
    (QUESTION_SOURCE_QUIZ, "Quiz"),
]

CONTRIBUTION_TYPE_LIST = [
    "nouvelle question",
    "commentaire application",
    "commentaire question",
    "commentaire quiz",
]

DEFAULT_DAILY_STAT_HOUR_SPLIT = {
    "0": {
        "question_answer_count": 0,
        "question_answer_from_quiz_count": 0,
        "quiz_answer_count": 0,
        "question_feedback_count": 0,
        "question_feedback_from_quiz_count": 0,
    },
    "1": {
        "question_answer_count": 0,
        "question_answer_from_quiz_count": 0,
        "quiz_answer_count": 0,
        "question_feedback_count": 0,
        "question_feedback_from_quiz_count": 0,
    },
    "2": {
        "question_answer_count": 0,
        "question_answer_from_quiz_count": 0,
        "quiz_answer_count": 0,
        "question_feedback_count": 0,
        "question_feedback_from_quiz_count": 0,
    },
    "3": {
        "question_answer_count": 0,
        "question_answer_from_quiz_count": 0,
        "quiz_answer_count": 0,
        "question_feedback_count": 0,
        "question_feedback_from_quiz_count": 0,
    },
    "4": {
        "question_answer_count": 0,
        "question_answer_from_quiz_count": 0,
        "quiz_answer_count": 0,
        "question_feedback_count": 0,
        "question_feedback_from_quiz_count": 0,
    },
    "5": {
        "question_answer_count": 0,
        "question_answer_from_quiz_count": 0,
        "quiz_answer_count": 0,
        "question_feedback_count": 0,
        "question_feedback_from_quiz_count": 0,
    },
    "6": {
        "question_answer_count": 0,
        "question_answer_from_quiz_count": 0,
        "quiz_answer_count": 0,
        "question_feedback_count": 0,
        "question_feedback_from_quiz_count": 0,
    },
    "7": {
        "question_answer_count": 0,
        "question_answer_from_quiz_count": 0,
        "quiz_answer_count": 0,
        "question_feedback_count": 0,
        "question_feedback_from_quiz_count": 0,
    },
    "8": {
        "question_answer_count": 0,
        "question_answer_from_quiz_count": 0,
        "quiz_answer_count": 0,
        "question_feedback_count": 0,
        "question_feedback_from_quiz_count": 0,
    },
    "9": {
        "question_answer_count": 0,
        "question_answer_from_quiz_count": 0,
        "quiz_answer_count": 0,
        "question_feedback_count": 0,
        "question_feedback_from_quiz_count": 0,
    },
    "10": {
        "question_answer_count": 0,
        "question_answer_from_quiz_count": 0,
        "quiz_answer_count": 0,
        "question_feedback_count": 0,
        "question_feedback_from_quiz_count": 0,
    },
    "11": {
        "question_answer_count": 0,
        "question_answer_from_quiz_count": 0,
        "quiz_answer_count": 0,
        "question_feedback_count": 0,
        "question_feedback_from_quiz_count": 0,
    },
    "12": {
        "question_answer_count": 0,
        "question_answer_from_quiz_count": 0,
        "quiz_answer_count": 0,
        "question_feedback_count": 0,
        "question_feedback_from_quiz_count": 0,
    },
    "13": {
        "question_answer_count": 0,
        "question_answer_from_quiz_count": 0,
        "quiz_answer_count": 0,
        "question_feedback_count": 0,
        "question_feedback_from_quiz_count": 0,
    },
    "14": {
        "question_answer_count": 0,
        "question_answer_from_quiz_count": 0,
        "quiz_answer_count": 0,
        "question_feedback_count": 0,
        "question_feedback_from_quiz_count": 0,
    },
    "15": {
        "question_answer_count": 0,
        "question_answer_from_quiz_count": 0,
        "quiz_answer_count": 0,
        "question_feedback_count": 0,
        "question_feedback_from_quiz_count": 0,
    },
    "16": {
        "question_answer_count": 0,
        "question_answer_from_quiz_count": 0,
        "quiz_answer_count": 0,
        "question_feedback_count": 0,
        "question_feedback_from_quiz_count": 0,
    },
    "17": {
        "question_answer_count": 0,
        "question_answer_from_quiz_count": 0,
        "quiz_answer_count": 0,
        "question_feedback_count": 0,
        "question_feedback_from_quiz_count": 0,
    },
    "18": {
        "question_answer_count": 0,
        "question_answer_from_quiz_count": 0,
        "quiz_answer_count": 0,
        "question_feedback_count": 0,
        "question_feedback_from_quiz_count": 0,
    },
    "19": {
        "question_answer_count": 0,
        "question_answer_from_quiz_count": 0,
        "quiz_answer_count": 0,
        "question_feedback_count": 0,
        "question_feedback_from_quiz_count": 0,
    },
    "20": {
        "question_answer_count": 0,
        "question_answer_from_quiz_count": 0,
        "quiz_answer_count": 0,
        "question_feedback_count": 0,
        "question_feedback_from_quiz_count": 0,
    },
    "21": {
        "question_answer_count": 0,
        "question_answer_from_quiz_count": 0,
        "quiz_answer_count": 0,
        "question_feedback_count": 0,
        "question_feedback_from_quiz_count": 0,
    },
    "22": {
        "question_answer_count": 0,
        "question_answer_from_quiz_count": 0,
        "quiz_answer_count": 0,
        "question_feedback_count": 0,
        "question_feedback_from_quiz_count": 0,
    },
    "23": {
        "question_answer_count": 0,
        "question_answer_from_quiz_count": 0,
        "quiz_answer_count": 0,
        "question_feedback_count": 0,
        "question_feedback_from_quiz_count": 0,
    },
}


def daily_stat_hour_split_jsonfield_default_value():
    return DEFAULT_DAILY_STAT_HOUR_SPLIT
