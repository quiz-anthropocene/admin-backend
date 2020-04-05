from django.db import models


class QuestionCategory(models.Model):
    name = models.CharField(max_length=50, blank=False, help_text="Le nom de la catégorie")
    name_long = models.CharField(max_length=150, blank=False, help_text="Le nom allongé de la catégorie")
    description = models.TextField(blank=True, help_text="Une description de la catégorie")
    created = models.DateField(auto_now=True, help_text="La date & heure de la création de la catégorie")

    def __str__(self):
        return f"{self.name}"

    @property
    def question_count(self):
        return self.questions.count()


class QuestionTag(models.Model):
    name = models.CharField(max_length=50, blank=False, help_text="Le nom du tag")
    description = models.TextField(blank=True, help_text="Une description du tag")
    created = models.DateField(auto_now=True, help_text="La date & heure de la création du tag")

    def __str__(self):
        return f"{self.name}"

    @property
    def question_count(self):
        return self.questions.count()


class QuestionQuerySet(models.QuerySet):
    def published(self):
        return self.exclude(publish=False)

    def for_category(self, category):
        return self.filter(category__name=category)

class Question(models.Model):
    QUESTION_TYPES = [
        ("QCM", "Questionnaire à choix multiples (QCM)"),
        ("VF", "Vrai ou Faux"),
    ]
    QUESTION_CATEGORIES = [
        ("biodiversité", "Biodiversité"),
        ("climat", "Climat"),
        ("consommation", "Consommation, Leviers d'action"),
        ("énergie", "Energie"),
        ("histoire", "Histoire, Anthropologie, Politique, Démographie"),
        ("pollution", "Pollution"),
        ("ressources", "Ressources (hors énergie)"),
        ("autre", "Autre"),
    ]
    QUESTION_DIFFICULTY = [
        (1, "Facile"),
        (2, "Moyen"),
        (3, "Difficile"),
        (4, "Expert")
    ]

    text = models.TextField(blank=False, help_text="La question en 1 ou 2 phrases")
    type = models.CharField(max_length=50, choices=QUESTION_TYPES, blank=False, help_text="Le type de question (QCM, V/F, ...)")
    category = models.ForeignKey(QuestionCategory, blank=False, null=True, on_delete=models.SET_NULL, related_name="questions", help_text="Une seule catégorie possible")
    tags = models.ManyToManyField(QuestionTag, blank=True, related_name="questions", help_text="Un ou plusieurs tags rattaché à la question")
    difficulty = models.IntegerField(choices=QUESTION_DIFFICULTY, blank=False, help_text="Le niveau de difficulté de la question")
    answer_option_a = models.CharField(max_length=150, help_text="La réponse a")
    answer_option_b = models.CharField(max_length=150, help_text="La réponse b")
    answer_option_c = models.CharField(max_length=150, help_text="La réponse c")
    answer_option_d = models.CharField(max_length=150, help_text="La réponse d")
    answer_correct = models.CharField(max_length=50, blank=False, help_text="a, b, c ou d")
    answer_explanation = models.TextField(blank=True, help_text="Un petit texte d'explication")
    answer_additional_link = models.URLField(max_length=500, blank=True, help_text="Un lien pour aller plus loin")
    answer_image_link = models.URLField(max_length=500, blank=True, help_text="Un lien vers une image pour illustrer la réponse (idéalement avec la source indiquée en bas de l'image)")
    answer_extra_info = models.TextField(blank=True, help_text="Texte et liens explicatifs additionels, qui n'apparaissent pas dans l'interface")
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
    def has_answer_additional_link(self):
        return len(self.answer_additional_link) > 0

    @property
    def has_answer_image_link(self):
        return len(self.answer_image_link) > 0

    @property
    def answer_count(self):
        return QuestionStat.objects.filter(question=self.id).count()

    @property
    def answer_success_count(self):
        return QuestionStat.objects.filter(question=self.id, answer_choice=self.answer_correct).count()

    @property
    def answer_success_rate(self):
        return 0 if (self.answer_count == 0) else int((self.answer_success_count / self.answer_count) * 100)

    # Admin
    answer_count.fget.short_description = "# Rép"
    answer_success_count.fget.short_description = "# Rép Corr"
    answer_success_rate.fget.short_description = "% Rép Corr"


class QuestionStat(models.Model):
    question = models.ForeignKey(
        Question, null=True, on_delete=models.CASCADE, related_name="stats"
    )
    answer_choice = models.CharField(max_length=50, editable=False, help_text="La réponse choisie par l'internaute")
    created = models.DateTimeField(auto_now=True, help_text="La date & heure de la réponse")


class Contribution(models.Model):
    text = models.TextField(blank=False, help_text="La contribution de l'utilisateur (une question ou un commentaire)")
    description = models.TextField(help_text="Informations supplémentaires sur la contribution (réponse, lien, ...)")
    is_question = models.BooleanField(default=True, help_text="La contribution est une question")
    created = models.DateTimeField(auto_now=True, help_text="La date & heure de la contribution")

    def __str__(self):
        return f"{self.text}"
