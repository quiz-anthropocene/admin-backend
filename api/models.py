from django.db import models


QUESTION_TYPES = [
    ("QCM", "Questionnaire à choix multiples (QCM)"),
    ("VF", "Vrai ou Faux"),
]

QUESTION_CATEGORIES = [
    ("Action", "Leviers d'action"),
    ("Biodiversité", "Biodiversité"),
    ("Climat", "Climat"),
    ("Consommation", "Consommation"),
    ("Energie", "Energie"),
    ("Histoire", "Histoire, Anthropologie"),
    ("Pollution", "Pollution"),
    ("Ressources", "Ressources (hors énergie)"),
    ("Science", "Science"),
    ("Autre", "Autre"),
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
    difficulty = models.IntegerField(choices=QUESTION_DIFFICULTY, blank=False, help_text="Niveau de difficulté de la question")
    answer_option_a = models.CharField(max_length=150)
    answer_option_b = models.CharField(max_length=150)
    answer_option_c = models.CharField(max_length=150)
    answer_option_d = models.CharField(max_length=150)
    answer_correct = models.CharField(max_length=50, blank=False, help_text="A, B, C ou D")
    answer_explanation = models.TextField(blank=True, help_text="Un petit texte d'explication")
    answer_additional_links = models.TextField(blank=True, help_text="Un ou des liens pour aller plus loin")
    created = models.DateField()
    updated = models.DateField()
