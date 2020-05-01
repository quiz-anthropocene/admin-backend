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
]
