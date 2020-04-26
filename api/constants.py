QUESTION_TYPES = [
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

# QUESTION_CATEGORIES = [
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
QUESTION_DIFFICULTY = [
    (0, "Junior"),
    (QUESTION_DIFFICULTY_EASY, "Facile"),
    (2, "Moyen"),
    (3, "Difficile"),
    (4, "Expert"),
]

QUESTION_SOUCE_QUESTION = "question"
QUESTION_SOUCE_QUIZ = "quiz"
QUESTION_SOUCE_CHOICES = [
    (QUESTION_SOUCE_QUESTION, "Question"),
    (QUESTION_SOUCE_QUIZ, "Quiz"),
]
