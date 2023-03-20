from django.utils.translation import gettext_lazy as _


QUESTION_TYPE_QCM = "QCM"
QUESTION_TYPE_QCM_RM = "QCM-RM"
QUESTION_TYPE_VF = "VF"
QUESTION_TYPE_CHOICES = [
    (QUESTION_TYPE_QCM, _("Multiple choice questionnaire")),
    (QUESTION_TYPE_QCM_RM, _("Multiple choice questionnaire with multiple answers")),
    (QUESTION_TYPE_VF, _("True or False")),
]
QUESTION_TYPE_CHOICE_LIST = [c[0] for c in QUESTION_TYPE_CHOICES]

QUESTION_TYPE_VF_CHOICE_LIST = ["a", "b"]
QUESTION_TYPE_QCM_CHOICE_LIST = ["a", "b", "c", "d"]

QUESTION_DIFFICULTY_JUNIOR = 0
QUESTION_DIFFICULTY_EASY = 1
QUESTION_DIFFICULTY_MEDIUM = 2
QUESTION_DIFFICULTY_HARD = 3
QUESTION_DIFFICULTY_EXPERT = 4
QUESTION_DIFFICULTY_OPTIONS = [
    (QUESTION_DIFFICULTY_JUNIOR, _("Junior"), "🧸"),
    (QUESTION_DIFFICULTY_EASY, _("Easy"), "🏆"),
    (QUESTION_DIFFICULTY_MEDIUM, _("Medium"), "🏆🏆"),
    (QUESTION_DIFFICULTY_HARD, _("Hard"), "🏆🏆🏆"),
    (QUESTION_DIFFICULTY_EXPERT, _("Expert"), "🏆🏆🏆🏆"),
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

VALIDATION_STATUS_DRAFT = "DRAFT"
VALIDATION_STATUS_TO_VALIDATE = "TO_VALIDATE"
VALIDATION_STATUS_VALIDATED = "VALIDATED"
VALIDATION_STATUS_ASIDE = "ASIDE"
VALIDATION_STATUS_REMOVED = "REMOVED"
VALIDATION_STATUS_CHOICES = [
    (VALIDATION_STATUS_DRAFT, _("Draft")),
    (VALIDATION_STATUS_TO_VALIDATE, _("To validate")),
    (VALIDATION_STATUS_VALIDATED, _("Validated")),
    (VALIDATION_STATUS_ASIDE, _("Set aside")),
    (VALIDATION_STATUS_REMOVED, _("Removed")),
]
VALIDATION_STATUS_CHOICE_LIST = [vs[0] for vs in VALIDATION_STATUS_CHOICES]

COMMENT_TYPE_NEW_QUESTION = "NEW_QUESTION"
COMMENT_TYPE_NEW_QUIZ = "NEW_QUIZ"
COMMENT_TYPE_COMMENT_APP = "COMMENT_APP"
COMMENT_TYPE_COMMENT_QUESTION = "COMMENT_QUESTION"
COMMENT_TYPE_COMMENT_QUIZ = "COMMENT_QUIZ"
COMMENT_TYPE_COMMENT_CONTRIBUTOR = "COMMENT_CONTRIBUTOR"
COMMENT_TYPE_REPLY = "REPLY"
COMMENT_TYPE_ERROR_APP = "ERROR_APP"
COMMENT_TYPE_CHOICES = [
    (COMMENT_TYPE_NEW_QUESTION, _("New question")),
    (COMMENT_TYPE_NEW_QUIZ, _("New quiz")),
    (COMMENT_TYPE_COMMENT_APP, _("Comment about the app")),
    (COMMENT_TYPE_COMMENT_QUESTION, _("Comment about a question")),
    (COMMENT_TYPE_COMMENT_QUIZ, _("Comment about a quiz")),
    (COMMENT_TYPE_COMMENT_CONTRIBUTOR, _("Contributor comment")),
    (COMMENT_TYPE_REPLY, _("Reply")),
    (COMMENT_TYPE_ERROR_APP, _("Application error")),
]

COMMENT_TYPE_REPLY_CHOICES = [
    (COMMENT_TYPE_COMMENT_CONTRIBUTOR, _("Comment")),
    (COMMENT_TYPE_REPLY, _("Answer")),
]

COMMENT_STATUS_NEW = "NEW"
COMMENT_STATUS_PENDING = "PENDING"
COMMENT_STATUS_PROCESSED = "PROCESSED"
COMMENT_STATUS_REPLIED = "REPLIED"
COMMENT_STATUS_IGNORED = "IGNORED"
COMMENT_STATUS_CHOICES = [
    (COMMENT_STATUS_NEW, _("To process")),
    (COMMENT_STATUS_PENDING, _("In progress")),
    (COMMENT_STATUS_PROCESSED, _("Processed")),
    (COMMENT_STATUS_REPLIED, _("Replied")),
    (COMMENT_STATUS_IGNORED, _("Ignored")),
]

LANGUAGE_FRENCH = "FRENCH"
LANGUAGE_ENGLISH = "ENGLISH"
LANGUAGE_SPANISH = "SPANISH"
LANGUAGE_ITALIAN = "ITALIAN"
LANGUAGE_GERMAN = "GERMAN"
LANGUAGE_OPTIONS = [
    (LANGUAGE_FRENCH, _("French"), "fr", "🇫🇷"),
    (LANGUAGE_ENGLISH, _("English"), "en", "🇬🇧"),
    (LANGUAGE_SPANISH, _("Spanish"), "es", "🇪🇸"),
    (LANGUAGE_ITALIAN, _("Italian"), "it", "🇮🇹"),
    (LANGUAGE_GERMAN, _("German"), "de", "🇩🇪"),
]
LANGUAGE_CHOICES = [(language[0], language[1]) for language in LANGUAGE_OPTIONS]
LANGUAGE_CHOICE_LIST = [language[0] for language in LANGUAGE_CHOICES]

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
    (VISIBILITY_PUBLIC, _("Public (exported and in the application)")),
    (VISIBILITY_HIDDEN, _("Hidden (exported but not visible in the application)")),
    (VISIBILITY_PRIVATE, _("Private (not exported and not in the application)")),
)

BOOLEAN_CHOICES = [(True, _("True")), (False, _("False"))]

EMPTY_CHOICE = (("", ""),)
