from django.db import models


class QuestionQuerySet(models.QuerySet):
    def published(self):
        return self.exclude(publish=False)

    def for_category(self, category):
        return self.filter(category=category)


class Question(models.Model):
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
    answer_image_link = models.TextField(blank=True, help_text="Un lien vers une image pour illustrer la réponse (idéalement avec la source indiquée en bas de l'image)")
    author = models.CharField(max_length=50, blank=True, help_text="L'auteur de la question")
    publish = models.BooleanField(default=False, blank=False, help_text="La question est prête à être publiée")
    created = models.DateField()
    updated = models.DateField()

    objects = QuestionQuerySet.as_manager()

    def __str__(self):
        return f"{self.text}"

    @property
    def has_answer_explanation(self):
        return len(self.answer_explanation) > 0

    @property
    def has_answer_additional_links(self):
        return len(self.answer_additional_links) > 0

    @property
    def has_answer_image_link(self):
        return len(self.answer_image_link) > 0

    @property
    def answer_count(self):
        return QuestionStat.objects.filter(question=self.id).count()

    @property
    def answer_success_count(self):
        return QuestionStat.objects.filter(question=self.id, answer_choice=self.answer_correct).count()

    # Admin
    has_answer_explanation.fget.short_description = "Explication"
    has_answer_additional_links.fget.short_description = "Lien(s)"
    has_answer_image_link.fget.short_description = "Image"
    answer_count.fget.short_description = "# Rép"
    answer_success_count.fget.short_description = "# Rép Corr"


class QuestionStat(models.Model):
    question = models.ForeignKey(
        Question, null=True, on_delete=models.CASCADE, related_name="stats"
    )
    answer_choice = models.CharField(max_length=50, editable=False, help_text="La réponse choisie par l'internaute")
    created = models.DateTimeField(auto_now=True, help_text="La date & heure de la réponse")


class Contribution(models.Model):
    text = models.TextField(blank=False)
    description = models.TextField()
    created = models.DateTimeField(auto_now=True, help_text="La date & heure de la contribution")

    def __str__(self):
        return f"{self.text}"
