QUESTION_TYPES = [
    ("QCM", "Questionnaire à choix multiples (QCM)"),
    ("VF", "Vrai ou Faux"),
]

QUESTION_VALIDATION_STATUS_NEW = "Nouvelle question"
QUESTION_VALIDATION_STATUS_LIST = [
    QUESTION_VALIDATION_STATUS_NEW,
    "En cours de validation",
    "Validée",
    "Écartée",
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

QUESTION_DIFFICULTY = [
    (0, "Junior"),
    (1, "Facile"),
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
