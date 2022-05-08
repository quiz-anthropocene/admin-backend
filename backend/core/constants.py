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
QUESTION_VALIDATION_STATUS_CHOICE_LIST = [
    QUESTION_VALIDATION_STATUS_NEW,
    QUESTION_VALIDATION_STATUS_IN_PROGRESS,
    QUESTION_VALIDATION_STATUS_OK,
    QUESTION_VALIDATION_STATUS_ASIDE,
    QUESTION_VALIDATION_STATUS_REMOVED,
]
QUESTION_VALIDATION_STATUS_CHOICES = [(vs, vs) for vs in QUESTION_VALIDATION_STATUS_CHOICE_LIST]

QUESTION_DIFFICULTY_EASY = 1
QUESTION_DIFFICULTY_HARD = 3
QUESTION_DIFFICULTY_OPTIONS = [
    (0, "Junior", "🧸"),
    (QUESTION_DIFFICULTY_EASY, "Facile", "🏆"),
    (2, "Moyen", "🏆🏆"),
    (QUESTION_DIFFICULTY_HARD, "Difficile", "🏆🏆🏆"),
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
QUESTION_ANSWER_CHOICES = [(a, a) for a in QUESTION_ANSWER_CHOICE_LIST]

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
CONTRIBUTION_TYPE_CHOICES = [(ct, ct) for ct in CONTRIBUTION_TYPE_LIST]

LANGUAGE_FRENCH = "Français"
LANGUAGE_ENGLISH = "English"
LANGUAGE_CHOICE_LIST = [
    LANGUAGE_FRENCH,
    LANGUAGE_ENGLISH,
]
LANGUAGE_CHOICES = [(lang, lang) for lang in LANGUAGE_CHOICE_LIST]

NOTION_QUESTIONS_IMPORT_SCOPE_CHOICES = [
    (0, "100 dernières questions modifiées"),
    # below are currently hidden
    (1, "1 à 200"),
    (2, "200 à 400"),
    (3, "400 à 600"),
    (4, "600 à 800"),
    (5, "800 et plus"),
]
NOTION_QUESTIONS_IMPORT_SCOPE_LIST = [value for (value, label) in NOTION_QUESTIONS_IMPORT_SCOPE_CHOICES]

VISIBILITY_PUBLIC = "PUBLIC"
VISIBILITY_HIDDEN = "HIDDEN"
VISIBILITY_PRIVATE = "PRIVATE"
VISIBILITY_CHOICES = (
    (VISIBILITY_PUBLIC, "Publique (dans l'export et dans l'application"),
    (VISIBILITY_HIDDEN, "Caché (dans l'export mais pas visible dans l'application)"),
    (VISIBILITY_PRIVATE, "Privé (pas dans l'export ni dans l'application)"),
)

BOOLEAN_CHOICES = [(True, "Vrai"), (False, "Faux")]

EMPTY_CHOICE = (("", ""),)
