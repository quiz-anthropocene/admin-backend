from django.db import models


QUESTION_TYPES = [
    ("QCM", "Questionnaire à choix multiples (QCM)"),
    ("VF", "Vrai ou Faux"),
]

QUESTION_CATEGORIES = [
    ("action", "Leviers d'action"),
    ("biodiversité", "Biodiversité"),
    ("climat", "Climat"),
    ("consommation", "Consommation"),
    ("énergie", "Energie"),
    ("histoire", "Histoire, Anthropologie"),
    ("pollution", "Pollution"),
    ("ressources", "Ressources (hors énergie)"),
    ("science", "Science"),
    ("autre", "Autre"),
]

QUESTION_DIFFICULTY = [
    (1, "Facile"),
    (2, "Moyen"),
    (3, "Difficile"),
    (4, "Expert")
]


class Question(models.Model):
    text = models.TextField(blank=False, help_text="La question en 1 ou 2 phrases")
    type = models.CharField(max_length=50, choices=QUESTION_TYPES, blank=False)
    category = models.CharField(max_length=50, choices=QUESTION_CATEGORIES, blank=False)
    difficulty = models.IntegerField(choices=QUESTION_DIFFICULTY, blank=False, help_text="Le niveau de difficulté de la question")
    answer_option_a = models.CharField(max_length=150, help_text="La réponse a")
    answer_option_b = models.CharField(max_length=150, help_text="La réponse b")
    answer_option_c = models.CharField(max_length=150, help_text="La réponse c")
    answer_option_d = models.CharField(max_length=150, help_text="La réponse d")
    answer_correct = models.CharField(max_length=50, blank=False, help_text="a, b, c ou d")
    answer_explanation = models.TextField(blank=True, help_text="Un petit texte d'explication")
    answer_additional_links = models.TextField(blank=True, help_text="Un ou des liens pour aller plus loin")
    author = models.CharField(max_length=50, blank=True, help_text="L'auteur de la question")
    publish = models.BooleanField(default=False, blank=False, help_text="La question est prête à être publiée")
    created = models.DateField()
    updated = models.DateField()
