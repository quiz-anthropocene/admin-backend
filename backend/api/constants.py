QUESTION_TYPE_QCM = "QCM"
QUESTION_TYPE_QCM_RM = "QCM-RM"
QUESTION_TYPE_VF = "VF"
QUESTION_TYPE_CHOICES = [
    (QUESTION_TYPE_QCM, "Questionnaire à choix multiples"),
    (QUESTION_TYPE_QCM_RM, "Questionnaire à choix multiples avec réponses multiples"),
    (QUESTION_TYPE_VF, "Vrai ou Faux"),
]
QUESTION_TYPE_CHOICE_LIST = [c[0] for c in QUESTION_TYPE_CHOICES]

QUESTION_TYPE_VF_CHOICE_LIST = ["a", "b"]
QUESTION_TYPE_QCM_CHOICE_LIST = ["a", "b", "c", "d"]

QUESTION_VALIDATION_STATUS_NEW = "Brouillon"
QUESTION_VALIDATION_STATUS_IN_PROGRESS = "A valider"
QUESTION_VALIDATION_STATUS_OK = "Validée"
QUESTION_VALIDATION_STATUS_ASIDE = "Écartée temporairement"
QUESTION_VALIDATION_STATUS_REMOVED = "Écartée"
QUESTION_VALIDATION_STATUS_LIST = [
    QUESTION_VALIDATION_STATUS_NEW,
    QUESTION_VALIDATION_STATUS_IN_PROGRESS,
    QUESTION_VALIDATION_STATUS_OK,
    QUESTION_VALIDATION_STATUS_ASIDE,
    QUESTION_VALIDATION_STATUS_REMOVED,
]

QUESTION_DIFFICULTY_EASY = 1
QUESTION_DIFFICULTY_OPTIONS = [
    (0, "Junior", "🧸"),
    (QUESTION_DIFFICULTY_EASY, "Facile", "🏆"),
    (2, "Moyen", "🏆🏆"),
    (3, "Difficile", "🏆🏆🏆"),
    (4, "Expert", "🏆🏆🏆🏆"),
]
QUESTION_DIFFICULTY_CHOICES = [(c[0], c[1]) for c in QUESTION_DIFFICULTY_OPTIONS]
QUESTION_DIFFICULTY_CHOICE_LIST = [c[0] for c in QUESTION_DIFFICULTY_OPTIONS]

QUESTION_ANSWER_CHOICE_LIST = [
    "a",
    "b",
    "c",
    "d",
    "ab",
    "ac",
    "ad",
    "bc",
    "bd",
    "cd",
    "abc",
    "abd",
    "acd",
    "bcd",
    "abcd",
]

QUIZ_RELATIONSHIP_CHOICE_LIST = [
    "suivant",
    # "précédent",
    "jumeau",
    "similaire",
    "traduction",
]

CONTRIBUTION_TYPE_LIST = [
    "nouvelle question",
    "nouveau quiz",
    "commentaire application",
    "commentaire question",
    "commentaire quiz",
    "nom application",
    "erreur application",
]

LANGUAGE_FRENCH = "Français"
LANGUAGE_ENGLISH = "English"
LANGUAGE_CHOICE_LIST = [
    LANGUAGE_FRENCH,
    LANGUAGE_ENGLISH,
]

NOTION_QUESTIONS_IMPORT_SCOPE_CHOICES = [
    (0, "tout"),
    (1, "1 à 200"),
    (2, "200 à 400"),
    (3, "400 à 600"),
    (4, "600 à 800"),
    (5, "800 et plus"),
]
NOTION_QUESTIONS_IMPORT_SCOPE_LIST = [
    value for (value, label) in NOTION_QUESTIONS_IMPORT_SCOPE_CHOICES
]
