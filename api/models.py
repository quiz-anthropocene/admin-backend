from django.db import models
from django.db.models import Avg, Sum
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError

from api import constants


class Category(models.Model):
    name = models.CharField(
        max_length=50, blank=False, help_text="Le nom de la catégorie"
    )
    name_long = models.CharField(
        max_length=150, blank=False, help_text="Le nom allongé de la catégorie"
    )
    description = models.TextField(
        blank=True, help_text="Une description de la catégorie"
    )
    created = models.DateField(
        auto_now_add=True, help_text="La date de création de la catégorie"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique category name")
        ]

    def __str__(self):
        return f"{self.name}"

    @property
    def question_count(self):
        return self.questions.published().count()


class TagManager(models.Manager):
    def get_ids_from_name_list(self, tag_name_list: list):
        tag_ids = []
        # Tag.objects.filter(name__in=tags_split) # ignores new tags
        for tag_name in tag_name_list:
            # tag, created = Tag.objects.get_or_create(name=tag_string)
            try:
                tag = Tag.objects.get(name=tag_name.strip())
            except Exception as e:
                raise type(e)(f"{tag_name}")
            tag_ids.append(tag.id)
        tag_ids.sort()
        return tag_ids


class Tag(models.Model):
    name = models.CharField(max_length=50, blank=False, help_text="Le nom du tag")
    description = models.TextField(blank=True, help_text="Une description du tag")
    created = models.DateField(
        auto_now_add=True, help_text="La date de création du tag"
    )

    objects = TagManager()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["name"], name="unique tag name")]

    def __str__(self):
        return f"{self.name}"

    @property
    def question_count(self):
        return self.questions.published().count()


class QuestionQuerySet(models.QuerySet):
    def published(self):
        return self.exclude(publish=False)

    def for_validation_status(self, validation_status):
        return self.filter(validation_status=validation_status)

    def for_category(self, category):
        return self.filter(category__name=category)

    def for_tag(self, tag):
        return self.filter(tags__name=tag)

    def for_author(self, author):
        return self.filter(author=author)

    def for_difficulty(self, difficulty):
        return self.filter(difficulty=difficulty)


class Question(models.Model):
    text = models.TextField(blank=False, help_text="La question en 1 ou 2 phrases")
    hint = models.TextField(blank=True, help_text="Un indice (optionnel)")
    type = models.CharField(
        max_length=50,
        choices=constants.QUESTION_TYPE_CHOICES,
        blank=False,
        help_text="Le type de question (QCM, V/F, ...)",
    )
    category = models.ForeignKey(
        Category,
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name="questions",
        help_text="Une seule catégorie possible",
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="questions",
        help_text="Un ou plusieurs tags rattaché à la question",
    )
    difficulty = models.IntegerField(
        choices=constants.QUESTION_DIFFICULTY_CHOICES,
        default=constants.QUESTION_DIFFICULTY_EASY,
        blank=False,
        help_text="Le niveau de difficulté de la question",
    )
    answer_option_a = models.CharField(max_length=150, help_text="La réponse a")
    answer_option_b = models.CharField(max_length=150, help_text="La réponse b")
    answer_option_c = models.CharField(
        max_length=150, blank=True, help_text="La réponse c"
    )
    answer_option_d = models.CharField(
        max_length=150, blank=True, help_text="La réponse d"
    )
    answer_correct = models.CharField(
        max_length=50,
        choices=zip(
            constants.QUESTION_ANSWER_CHOICE_LIST,
            constants.QUESTION_ANSWER_CHOICE_LIST,
        ),
        help_text="a, b, c ou d",
    )
    has_ordered_answers = models.BooleanField(
        default=True,
        help_text="Les choix de réponse sont dans un ordre figé, "
        "et ne doivent pas être mélangés",
    )
    answer_explanation = models.TextField(
        blank=True, help_text="Un petit texte d'explication"
    )
    answer_accessible_url = models.URLField(
        max_length=500, blank=True, help_text="Un lien pour aller plus loin"
    )
    answer_scientific_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="La source scientifique du chiffre (rapport)",
    )
    answer_image_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="Un lien vers une image pour illustrer la réponse "
        "(idéalement avec la source indiquée en bas de l'image)",
    )
    answer_image_explanation = models.TextField(
        blank=True, help_text="Une légende pour l'image qui illustre la réponse"
    )
    answer_extra_info = models.TextField(
        blank=True,
        help_text="Texte et liens explicatifs additionels, qui n'apparaissent pas "
        "dans l'interface",
    )
    author = models.CharField(
        max_length=50, blank=True, help_text="L'auteur de la question"
    )
    validator = models.CharField(
        max_length=50, blank=True, help_text="La personne qui a validée la question"
    )
    publish = models.BooleanField(
        default=False, help_text="La question est prête à être publiée"
    )
    validation_status = models.CharField(
        max_length=150,
        choices=zip(
            constants.QUESTION_VALIDATION_STATUS_LIST,
            constants.QUESTION_VALIDATION_STATUS_LIST,
        ),
        default=constants.QUESTION_VALIDATION_STATUS_NEW,
        help_text="Le statut de la question dans le workflow de validation",
    )
    # stats
    answer_count = models.PositiveIntegerField(
        default=0, help_text="Le nombre de réponses"
    )
    answer_success_count = models.PositiveIntegerField(
        default=0, help_text="Le nombre de réponses correctes"
    )
    like_count = models.PositiveIntegerField(default=0, help_text="Le nombre de likes")
    dislike_count = models.PositiveIntegerField(
        default=0, help_text="Le nombre de dislikes"
    )
    # timestamps
    added = models.DateField(
        blank=True, null=True, help_text="La date d'ajout de la question"
    )
    created = models.DateField(
        auto_now_add=True, help_text="La date de création de la question"
    )
    updated = models.DateField(auto_now=True)

    objects = QuestionQuerySet.as_manager()

    def __str__(self):
        return f"{self.id} - {self.category} - {self.text}"

    @property
    def tags_list(self):
        return list(self.tags.values_list("name", flat=True))

    @property
    def tags_list_string(self):
        return ", ".join(self.tags_list)

    @property
    def has_hint(self):
        return len(self.hint) > 0

    @property
    def has_answer_explanation(self):
        return len(self.answer_explanation) > 0

    @property
    def has_answer_accessible_url(self):
        return len(self.answer_accessible_url) > 0

    @property
    def has_answer_scientific_url(self):
        return len(self.answer_scientific_url) > 0

    @property
    def has_answer_image_url(self):
        return len(self.answer_image_url) > 0

    @property
    def answer_count_agg(self):
        return self.agg_stats.answer_count + self.stats.count()

    @property
    def answer_success_count_agg(self):
        return (
            self.agg_stats.answer_success_count
            + self.stats.filter(choice=self.answer_correct).count()
        )

    @property
    def answer_success_rate(self):
        return (
            0
            if (self.answer_count_agg == 0)
            else int((self.answer_success_count_agg / self.answer_count_agg) * 100)
        )

    @property
    def like_count_agg(self):
        return self.agg_stats.like_count + self.feedbacks.liked().count()

    @property
    def dislike_count_agg(self):
        return self.agg_stats.dislike_count + self.feedbacks.disliked().count()

    # Admin
    tags_list_string.fget.short_description = "Tag(s)"
    answer_count_agg.fget.short_description = "# Rép"
    answer_success_count_agg.fget.short_description = "# Rép Corr"
    answer_success_rate.fget.short_description = "% Rép Corr"
    like_count_agg.fget.short_description = "# Like"
    dislike_count_agg.fget.short_description = "# Dislike"


def question_validate_fields(sender, instance, **kwargs):
    """
    Method to validate Question fields. Why ?
    - ModelFields with choices are validated only in forms, but not during loaddata (and test fixtures) # noqa
    - https://zindilis.com/blog/2017/05/04/django-backend-validation-of-choices.html
    - https://adamj.eu/tech/2020/01/22/djangos-field-choices-dont-constrain-your-data/
    """
    # only run on soon-to-be and validated questions
    if getattr(instance, "validation_status") not in [
        constants.QUESTION_VALIDATION_STATUS_NEW,
        constants.QUESTION_VALIDATION_STATUS_REMOVED,
    ]:
        # > relation fields: "category" & "tags" ? no need
        # checks will be done automatically to validate the existence of the foreign key.
        # > choice fields
        question_choice_fields = [
            ("type", "QUESTION_TYPE_CHOICE_LIST"),
            ("difficulty", "QUESTION_DIFFICULTY_CHOICE_LIST"),
            ("answer_correct", "QUESTION_ANSWER_CHOICE_LIST"),
            ("validation_status", "QUESTION_VALIDATION_STATUS_LIST"),
        ]
        for choice_field in question_choice_fields:
            if getattr(instance, choice_field[0]) not in getattr(
                constants, choice_field[1]
            ):  # noqa
                raise ValidationError(
                    f"Question pre_save error. Field {choice_field[0]}. "
                    f"Value given: '{getattr(instance, choice_field[0])}'. "
                    f"Question: {instance}"
                )
        # > other rules
        # - Vrai/Faux question must have answer_correct equal to 'a' or 'b'
        # - Vrai/Faux question must have has_ordered_answers checked
        if getattr(instance, "type") == constants.QUESTION_TYPE_VF:
            if getattr(instance, "answer_correct") not in ["a", "b"]:
                raise ValidationError(
                    f"Question pre_save error. Type VF & Field answer_correct. "
                    f"Value given: '{getattr(instance, 'answer_correct')}'. "
                    f"Question: {instance}"
                )
            if not getattr(instance, "has_ordered_answers"):
                raise ValidationError(
                    f"Question pre_save error. Type VF & Field has_ordered_answers. "
                    f"Value given: '{getattr(instance, 'has_ordered_answers')}'. "
                    f"Question: {instance}"
                )


def question_create_agg_stat_instance(sender, instance, created, **kwargs):
    if created:
        if not hasattr(instance, "agg_stats"):
            QuestionAggStat.objects.create(question=instance)


models.signals.pre_save.connect(question_validate_fields, sender=Question)
models.signals.post_save.connect(question_create_agg_stat_instance, sender=Question)


class QuestionAggStat(models.Model):
    question = models.OneToOneField(
        Question, on_delete=models.CASCADE, primary_key=True, related_name="agg_stats"
    )
    answer_count = models.PositiveIntegerField(
        default=0, help_text="Le nombre de réponses"
    )
    answer_success_count = models.PositiveIntegerField(
        default=0, help_text="Le nombre de réponses correctes"
    )
    like_count = models.PositiveIntegerField(default=0, help_text="Le nombre de likes")
    dislike_count = models.PositiveIntegerField(
        default=0, help_text="Le nombre de dislikes"
    )


class QuestionAnswerEvent(models.Model):
    question = models.ForeignKey(
        Question, null=True, on_delete=models.CASCADE, related_name="stats"
    )
    choice = models.CharField(
        max_length=50,
        choices=zip(
            constants.QUESTION_ANSWER_CHOICE_LIST,
            constants.QUESTION_ANSWER_CHOICE_LIST,
        ),
        editable=False,
        help_text="La réponse choisie par l'internaute",
    )
    source = models.CharField(
        max_length=50,
        choices=constants.QUESTION_SOURCE_CHOICES,
        default=constants.QUESTION_SOURCE_QUESTION,
        editable=False,
        help_text="Le contexte dans lequel a été répondu la question",
    )
    created = models.DateTimeField(
        auto_now_add=True, help_text="La date & heure de la réponse"
    )


class QuestionFeedbackEventQuerySet(models.QuerySet):
    def liked(self):
        return self.filter(choice=constants.FEEDBACK_LIKE)

    def disliked(self):
        return self.filter(choice=constants.FEEDBACK_DISLIKE)


class QuestionFeedbackEvent(models.Model):
    question = models.ForeignKey(
        Question, null=True, on_delete=models.CASCADE, related_name="feedbacks"
    )
    choice = models.CharField(
        max_length=50,
        choices=constants.FEEDBACK_CHOICES,
        default=constants.FEEDBACK_LIKE,
        editable=False,
        help_text="L'avis laissé sur la question",
    )
    source = models.CharField(
        max_length=50,
        choices=constants.QUESTION_SOURCE_CHOICES,
        default=constants.QUESTION_SOURCE_QUESTION,
        editable=False,
        help_text="Le contexte dans lequel a été envoyé l'avis",
    )
    created = models.DateTimeField(
        auto_now_add=True, help_text="La date & heure de l'avis"
    )

    objects = QuestionFeedbackEventQuerySet.as_manager()


class QuizQuerySet(models.QuerySet):
    def published(self):
        return self.exclude(publish=False)

    def for_author(self, author):
        return self.filter(author=author)


class Quiz(models.Model):
    name = models.CharField(max_length=50, blank=False, help_text="Le nom du quiz")
    description = models.TextField(blank=True, help_text="Une description du quiz")
    questions = models.ManyToManyField(
        Question, related_name="quizzes", help_text="Les questions du quiz"
    )
    author = models.CharField(max_length=50, blank=True, help_text="L'auteur du quiz")
    image_background_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="Un lien vers une image pour illustrer le quiz",
    )
    publish = models.BooleanField(
        default=False, help_text="Le quiz est prêt à être publié"
    )
    # stats
    # answer_count
    like_count = models.PositiveIntegerField(default=0, help_text="Le nombre de likes")
    dislike_count = models.PositiveIntegerField(
        default=0, help_text="Le nombre de dislikes"
    )
    # timestamps
    created = models.DateField(
        auto_now_add=True, help_text="La date de création du quiz"
    )

    objects = QuizQuerySet.as_manager()

    def __str__(self):
        return f"{self.name}"

    @property
    def question_count(self):
        return self.questions.count()  # published() ?

    @property
    def categories_list(self):
        # self.questions.values("category__name").annotate(count=Count('category__name')).order_by("-count")
        return list(
            self.questions.order_by()
            .values_list("category__name", flat=True)
            .distinct()
        )  # .sort()
        # from collections import Counter
        # counter = Counter(self.questions.values_list("category__name", flat=True))
        # return sorted(counter, key=counter.get, reverse=True)

    @property
    def categories_list_string(self):
        return ", ".join(self.categories_list)

    @property
    def tags_list(self):
        return list(
            self.questions.order_by().values_list("tags__name", flat=True).distinct()
        )

    @property
    def tags_list_string(self):
        return ", ".join(self.tags_list)

    @property
    def difficulty_average(self):
        difficulty_average = self.questions.aggregate(Avg("difficulty"))
        return difficulty_average["difficulty__avg"] if difficulty_average else 0

    @property
    def like_count_agg(self):
        return self.like_count + self.feedbacks.liked().count()

    @property
    def dislike_count_agg(self):
        return self.dislike_count + self.feedbacks.disliked().count()

    @property
    def answer_count_agg(self):
        return self.stats.count()

    # Admin
    categories_list_string.fget.short_description = "Catégorie(s)"
    tags_list_string.fget.short_description = "Tag(s)"
    difficulty_average.fget.short_description = "Difficulté moyenne"
    answer_count_agg.fget.short_description = "# Rép"
    like_count_agg.fget.short_description = "# Like"
    dislike_count_agg.fget.short_description = "# Dislike"


def quiz_validate_m2m_fields(sender, **kwargs):
    """
    Method to validate Quiz fields. Why ?
    see question_validate_fields
    """
    # only run on published quizzes
    if getattr(kwargs["instance"], "publish"):
        # > relation fields: check that the quiz's questions are published
        if kwargs["instance"] and kwargs["action"] == "pre_add":
            qlist = (
                Question.objects.filter(pk__in=kwargs["pk_set"])
                .published()
                .values_list("id", flat=True)
            )
            if len(kwargs["pk_set"]) != len(list(qlist)):
                raise ValidationError(
                    f"Quiz pre_save_m2m error. Relation questions. "
                    f"Questions count: {len(kwargs['pk_set'])}. Questions published count: {len(list(qlist))}. "  # noqa
                    f"Unpublished questions: {[el for el in kwargs['pk_set'] if el not in list(qlist)]}"  # noqa
                )


models.signals.m2m_changed.connect(
    quiz_validate_m2m_fields, sender=Quiz.questions.through
)


class QuizAnswerEvent(models.Model):
    quiz = models.ForeignKey(
        Quiz, null=True, on_delete=models.CASCADE, related_name="stats"
    )
    answer_success_count = models.IntegerField(
        editable=False,
        help_text="La nombre de réponses correctes trouvées par l'internaute",
    )
    created = models.DateTimeField(
        auto_now_add=True, help_text="La date & heure de la réponse"
    )

    @property
    def question_count(self):
        return self.quiz.question_count


class QuizFeedbackEventQuerySet(models.QuerySet):
    def liked(self):
        return self.filter(choice=constants.FEEDBACK_LIKE)

    def disliked(self):
        return self.filter(choice=constants.FEEDBACK_DISLIKE)


class QuizFeedbackEvent(models.Model):
    quiz = models.ForeignKey(
        Quiz, null=True, on_delete=models.CASCADE, related_name="feedbacks"
    )
    choice = models.CharField(
        max_length=50,
        choices=constants.FEEDBACK_CHOICES,
        default=constants.FEEDBACK_LIKE,
        editable=False,
        help_text="L'avis laissé sur le quiz",
    )
    created = models.DateTimeField(
        auto_now_add=True, help_text="La date & heure de l'avis"
    )

    objects = QuizFeedbackEventQuerySet.as_manager()


class Contribution(models.Model):
    text = models.TextField(
        blank=False,
        help_text="La contribution de l'utilisateur (une question ou un commentaire)",
    )
    description = models.TextField(
        help_text="Informations supplémentaires sur la contribution (réponse, lien, ...)"
    )
    type = models.CharField(
        max_length=150,
        choices=zip(
            constants.CONTRIBUTION_TYPE_LIST, constants.CONTRIBUTION_TYPE_LIST,
        ),
        blank=True,
        help_text="Le type de contribution",
    )
    created = models.DateTimeField(
        auto_now_add=True, help_text="La date & heure de la contribution"
    )

    def __str__(self):
        return f"{self.text}"


class Glossary(models.Model):
    name = models.CharField(max_length=50, blank=False, help_text="Le mot ou sigle")
    name_alternatives = models.TextField(
        blank=True, help_text="Des noms alternatifs"
    )  # ArrayField
    definition_short = models.CharField(
        max_length=150, blank=False, help_text="La definition succinte du mot"
    )
    description = models.TextField(
        blank=True, help_text="Une description longue du mot"
    )
    description_accessible_url = models.URLField(
        max_length=500, blank=True, help_text="Un lien pour aller plus loin"
    )
    # timestamps
    added = models.DateField(blank=True, null=True, help_text="La date d'ajout du mot")
    created = models.DateField(
        auto_now_add=True, help_text="La date de création du mot"
    )
    updated = models.DateField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique glossary name")
        ]

    def __str__(self):
        return f"{self.name}"


class DailyStatManager(models.Manager):
    def overall_question_answer_count(self):
        return self.aggregate(Sum("question_answer_count"))[
            "question_answer_count__sum"
        ]

    def overall_question_answer_from_quiz_count(self):
        return self.aggregate(Sum("question_answer_from_quiz_count"))[
            "question_answer_from_quiz_count__sum"
        ]

    def overall_quiz_answer_count(self):
        return self.aggregate(Sum("quiz_answer_count"))["quiz_answer_count__sum"]

    def overall_question_feedback_count(self):
        return self.aggregate(Sum("question_feedback_count"))[
            "question_feedback_count__sum"
        ]

    def overall_question_feedback_from_quiz_count(self):
        return self.aggregate(Sum("question_feedback_from_quiz_count"))[
            "question_feedback_from_quiz_count__sum"
        ]


class DailyStat(models.Model):
    date = models.DateField(help_text="Le jour de la statistique")
    question_answer_count = models.PositiveIntegerField(
        default=0, help_text="Le nombre de questions répondues"
    )
    question_answer_from_quiz_count = models.PositiveIntegerField(
        default=0, help_text="Le nombre de questions répondues au sein de quizs"
    )
    quiz_answer_count = models.PositiveIntegerField(
        default=0, help_text="Le nombre de quizs répondus"
    )
    question_feedback_count = models.PositiveIntegerField(
        default=0, help_text="Le nombre de feedbacks aux questions"
    )
    question_feedback_from_quiz_count = models.PositiveIntegerField(
        default=0, help_text="Le nombre de feedbacks aux questions au sein de quizs"
    )
    quiz_feedback_count = models.PositiveIntegerField(
        default=0, help_text="Le nombre de feedbacks aux quizs"
    )
    hour_split = JSONField(
        default=constants.daily_stat_hour_split_jsonfield_default_value,
        help_text="Les statistiques par heure",
    )
    created = models.DateTimeField(
        auto_now_add=True, help_text="La date & heure de la stat journalière"
    )

    objects = DailyStatManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["date"], name="unique stat date")
        ]

    def __str__(self):
        return f"{self.date}"
