from django.db import models


class QuestionCategory(models.Model):
    name = models.CharField(max_length=50, blank=False, help_text="Le nom de la catégorie")
    name_long = models.CharField(max_length=150, blank=False, help_text="Le nom allongé de la catégorie")
    description = models.TextField(blank=True, help_text="Une description de la catégorie")
    created = models.DateField(auto_now=True, help_text="La date & heure de la création de la catégorie")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique category name')
        ]

    def __str__(self):
        return f"{self.name}"

    @property
    def question_count(self):
        return self.questions.count() # published() ?


class QuestionTag(models.Model):
    name = models.CharField(max_length=50, blank=False, help_text="Le nom du tag")
    description = models.TextField(blank=True, help_text="Une description du tag")
    created = models.DateField(auto_now=True, help_text="La date & heure de la création du tag")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique tag name')
        ]

    def __str__(self):
        return f"{self.name}"

    @property
    def question_count(self):
        return self.questions.count() # published() ?


class QuestionQuerySet(models.QuerySet):
    def published(self):
        return self.exclude(publish=False)

    def for_category(self, category):
        return self.filter(category__name=category)

    def for_tag(self, tag):
        return self.filter(tags__name=tag)

    def for_author(self, author):
        return self.filter(author=author)

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
    answer_option_c = models.CharField(max_length=150, blank=True, help_text="La réponse c")
    answer_option_d = models.CharField(max_length=150, blank=True, help_text="La réponse d")
    answer_correct = models.CharField(max_length=50, help_text="a, b, c ou d")
    has_ordered_answers = models.BooleanField(default=True, help_text="Les choix de réponse sont dans un ordre figé, et ne doivent pas être mélangés")
    answer_explanation = models.TextField(blank=True, help_text="Un petit texte d'explication")
    answer_additional_link = models.URLField(max_length=500, blank=True, help_text="Un lien pour aller plus loin")
    answer_image_link = models.URLField(max_length=500, blank=True, help_text="Un lien vers une image pour illustrer la réponse (idéalement avec la source indiquée en bas de l'image)")
    answer_extra_info = models.TextField(blank=True, help_text="Texte et liens explicatifs additionels, qui n'apparaissent pas dans l'interface")
    author = models.CharField(max_length=50, blank=True, help_text="L'auteur de la question")
    publish = models.BooleanField(default=False, help_text="La question est prête à être publiée")
    created = models.DateField()
    updated = models.DateField()

    objects = QuestionQuerySet.as_manager()

    def __str__(self):
        return f"{self.id} - {self.category} - {self.text}"

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
        return self.stats.count()

    @property
    def answer_success_count(self):
        return self.stats.filter(answer_choice=self.answer_correct).count()

    @property
    def answer_success_rate(self):
        return 0 if (self.answer_count == 0) else int((self.answer_success_count / self.answer_count) * 100)

    # Admin
    answer_count.fget.short_description = "# Rép"
    answer_success_count.fget.short_description = "# Rép Corr"
    answer_success_rate.fget.short_description = "% Rép Corr"


class QuizQuerySet(models.QuerySet):
    def published(self):
        return self.exclude(publish=False)

    def for_author(self, author):
        return self.filter(author=author)

class Quiz(models.Model):
    name = models.CharField(max_length=50, blank=False, help_text="Le nom du quiz")
    description = models.TextField(blank=True, help_text="Une description du quiz")
    questions = models.ManyToManyField(Question, related_name="quizzes", help_text="Les questions du quiz")
    author = models.CharField(max_length=50, blank=True, help_text="L'auteur du quiz")
    publish = models.BooleanField(default=False, help_text="Le quiz est prêt à être publié")
    created = models.DateField(auto_now=True, help_text="La date & heure de la création du quiz")

    objects = QuizQuerySet.as_manager()

    def __str__(self):
        return f"{self.name}"

    @property
    def question_count(self):
        return self.questions.count() # published() ?

    @property
    def categories(self):
        # self.questions.values("category__name").annotate(count=Count('category__name')).order_by("-count")
        return list(self.questions.order_by().values_list("category__name", flat=True).distinct()) # .sort()
        # from collections import Counter
        # counter = Counter(self.questions.values_list("category__name", flat=True))
        # return sorted(counter, key=counter.get, reverse=True)

    @property
    def tags(self):
        return list(self.questions.order_by().values_list("tags__name", flat=True).distinct())

    @property
    def answer_count(self):
        return self.stats.count()


class QuestionStat(models.Model):
    QUESTION_SOUCE_QUESTION = "question"
    QUESTION_SOUCE_QUIZ = "quiz"
    QUESTION_SOUCE_CHOICES = [
        (QUESTION_SOUCE_QUESTION, "Question"),
        (QUESTION_SOUCE_QUIZ, "Quiz")
    ]

    question = models.ForeignKey(
        Question, null=True, on_delete=models.CASCADE, related_name="stats"
    )
    answer_choice = models.CharField(max_length=50, editable=False, help_text="La réponse choisie par l'internaute")
    source = models.CharField(max_length=50, choices=QUESTION_SOUCE_CHOICES, default=QUESTION_SOUCE_QUESTION, editable=False, help_text="Le contexte dans lequel a été répondu la question")
    created = models.DateTimeField(auto_now=True, help_text="La date & heure de la réponse")


class QuizStat(models.Model):
    quiz = models.ForeignKey(
        Quiz, null=True, on_delete=models.CASCADE, related_name="stats"
    )
    answer_success_count = models.IntegerField(editable=False, help_text="La nombre de réponses correctes trouvées par l'internaute")
    created = models.DateTimeField(auto_now=True, help_text="La date & heure de la réponse")


class Contribution(models.Model):
    text = models.TextField(blank=False, help_text="La contribution de l'utilisateur (une question ou un commentaire)")
    description = models.TextField(help_text="Informations supplémentaires sur la contribution (réponse, lien, ...)")
    is_question = models.BooleanField(default=True, help_text="La contribution est une question")
    created = models.DateTimeField(auto_now=True, help_text="La date & heure de la contribution")

    def __str__(self):
        return f"{self.text}"
