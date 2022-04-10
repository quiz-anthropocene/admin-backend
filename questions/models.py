from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from core import constants
from core.utils import utilities
from tags.models import Tag


class QuestionQuerySet(models.QuerySet):
    def validated(self):
        return self.filter(validation_status=constants.QUESTION_VALIDATION_STATUS_OK)

    def not_validated(self):
        return self.exclude(validation_status=constants.QUESTION_VALIDATION_STATUS_OK)

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
    QUESTION_CHOICE_FIELDS = [
        "type",
        "difficulty",
        "language",
        "answer_correct",
        "validation_status",
        "author",
        "validator",
    ]
    QUESTION_FK_FIELDS = ["category"]
    QUESTION_M2M_FIELDS = ["tags"]
    QUESTION_BOOLEAN_FIELDS = ["has_ordered_answers"]
    QUESTION_URL_FIELDS = ["answer_audio", "answer_video", "answer_accessible_url", "answer_scientific_url"]
    QUESTION_IMAGE_URL_FIELDS = ["answer_image_url"]

    text = models.TextField(blank=False, help_text="La question en 1 ou 2 phrases")
    hint = models.TextField(blank=True, help_text="Un indice (optionnel)")
    type = models.CharField(
        max_length=50,
        choices=constants.QUESTION_TYPE_CHOICES,
        default=constants.QUESTION_TYPE_QCM,
        blank=False,
        help_text="Le type de question (QCM, V/F, ...)",
    )
    category = models.ForeignKey(
        "categories.Category",
        blank=True,
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
    language = models.CharField(
        max_length=50,
        choices=constants.LANGUAGE_CHOICES,
        default=constants.LANGUAGE_FRENCH,
        blank=False,
        help_text="La langue de la question",
    )
    answer_option_a = models.CharField(max_length=500, blank=True, help_text="La réponse a")
    answer_option_b = models.CharField(max_length=500, blank=True, help_text="La réponse b")
    answer_option_c = models.CharField(max_length=500, blank=True, help_text="La réponse c")
    answer_option_d = models.CharField(max_length=500, blank=True, help_text="La réponse d")
    answer_correct = models.CharField(
        max_length=50,
        choices=constants.QUESTION_ANSWER_CHOICES,
        blank=True,
        help_text="a, b, c ou d. ab, acd, abcd, etc si plusieurs réponses.",
    )
    has_ordered_answers = models.BooleanField(
        default=True,
        help_text="Les choix de réponse sont dans un ordre figé, " "et ne doivent pas être mélangés",
    )
    answer_explanation = models.TextField(blank=True, help_text="Un petit texte d'explication")
    answer_audio = models.URLField(max_length=500, blank=True, help_text="Une explication audio")
    answer_video = models.URLField(max_length=500, blank=True, help_text="Une explication vidéo")
    answer_accessible_url = models.URLField(max_length=500, blank=True, help_text="Un lien pour aller plus loin")
    answer_accessible_url_text = models.CharField(
        max_length=500,
        blank=True,
        help_text="Le texte pour remplace l'affichage du lien",
    )
    answer_scientific_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="La source scientifique du chiffre (rapport)",
    )
    answer_scientific_url_text = models.CharField(
        max_length=500,
        blank=True,
        help_text="Le texte pour remplace l'affichage du lien de la source scientifique",  # noqa
    )
    answer_reading_recommendation = models.TextField(blank=True, help_text="Un livre pour aller plus loin")
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
        help_text="Texte et liens explicatifs additionels, qui n'apparaissent pas " "dans l'interface",
    )
    author = models.CharField(max_length=50, blank=True, help_text="L'auteur de la question")
    validator = models.CharField(max_length=50, blank=True, help_text="La personne qui a validée la question")
    validation_status = models.CharField(
        max_length=150,
        choices=constants.QUESTION_VALIDATION_STATUS_CHOICES,
        default=constants.QUESTION_VALIDATION_STATUS_NEW,
        help_text="Le statut de la question dans le workflow de validation",
    )
    # timestamps
    added = models.DateField(blank=True, null=True, help_text="La date d'ajout de la question")
    created = models.DateField(auto_now_add=True, help_text="La date de création de la question")
    updated = models.DateField(auto_now=True)

    objects = QuestionQuerySet.as_manager()

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ["pk"]

    def __str__(self):
        return f"{self.id} - {self.category} - {self.text}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Question, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("questions:detail", kwargs={"pk": self.id})

    @property
    def tags_list(self) -> list:
        return list(self.tags.values_list("name", flat=True))

    @property
    def tags_list_string(self) -> str:
        return ", ".join(self.tags_list)

    @property
    def quizs_list(self) -> list:
        return list(self.quizs.values_list("name", flat=True))

    @property
    def quizs_list_string(self) -> str:
        return ", ".join(self.quizs_list)

    @property
    def has_hint(self) -> bool:
        return len(self.hint) > 0

    @property
    def has_answer_explanation(self) -> bool:
        return len(self.answer_explanation) > 0

    @property
    def has_answer_audio(self) -> bool:
        return len(self.answer_audio) > 0

    @property
    def has_answer_video(self) -> bool:
        return len(self.answer_video) > 0

    @property
    def has_answer_accessible_url(self) -> bool:
        return len(self.answer_accessible_url) > 0

    @property
    def has_answer_scientific_url(self) -> bool:
        return len(self.answer_scientific_url) > 0

    @property
    def has_answer_image_url(self) -> bool:
        return len(self.answer_image_url) > 0

    @property
    def answer_count_agg(self) -> int:
        return self.agg_stats.answer_count + self.stats.count()

    @property
    def answer_success_count_agg(self) -> int:
        return self.agg_stats.answer_success_count + self.stats.filter(choice=self.answer_correct).count()

    @property
    def answer_success_rate(self) -> int:
        return (
            0 if (self.answer_count_agg == 0) else int((self.answer_success_count_agg / self.answer_count_agg) * 100)
        )

    @property
    def like_count_agg(self) -> int:
        return self.agg_stats.like_count + self.feedbacks.liked().count()

    @property
    def dislike_count_agg(self) -> int:
        return self.agg_stats.dislike_count + self.feedbacks.disliked().count()

    # Admin
    tags_list_string.fget.short_description = "Tag(s)"
    quizs_list_string.fget.short_description = "Quiz(s)"
    answer_count_agg.fget.short_description = "# Rép"
    answer_success_count_agg.fget.short_description = "# Rép Corr"
    answer_success_rate.fget.short_description = "% Rép Corr"
    like_count_agg.fget.short_description = "# Like"
    dislike_count_agg.fget.short_description = "# Dislike"

    # def question_validate_fields(sender, instance, **kwargs):
    def clean(self):
        # dict to store all ValidationErrors
        validation_errors = dict()
        """
        Method to validate Question fields. Why ?
        - ModelFields with choices are validated only in forms, but not during loaddata (and test fixtures) # noqa
        - https://zindilis.com/blog/2017/05/04/django-backend-validation-of-choices.html
        - https://adamj.eu/tech/2020/01/22/djangos-field-choices-dont-constrain-your-data/
        """
        # > only run on validated questions
        if self.validation_status == constants.QUESTION_VALIDATION_STATUS_OK:
            # > category rules
            if self.category is None:
                error_message = (
                    f"Valeur : '{self.category}' n'est pas une catégorie valide. Question {self.id}"  # noqa
                )
                validation_errors = utilities.add_validation_error(validation_errors, "category", error_message)
            # > relation fields: "category" & "tags" ? no need
            # checks will be done automatically to validate the existence of the foreign key.
            # > fields with choices rules
            question_choice_fields = [
                ("type", "QUESTION_TYPE_CHOICE_LIST"),
                ("difficulty", "QUESTION_DIFFICULTY_CHOICE_LIST"),
                ("language", "LANGUAGE_CHOICE_LIST"),
                ("answer_correct", "QUESTION_ANSWER_CHOICE_LIST"),
                # ("validation_status", "QUESTION_VALIDATION_STATUS_LIST"),
            ]
            for choice_field in question_choice_fields:
                if getattr(self, choice_field[0]) not in getattr(constants, choice_field[1]):
                    error_message = f"Valeur : '{getattr(self, choice_field[0])}' n'est pas bonne. Car pas dans les choix proposés. Question {self.id}"  # noqa
                    validation_errors = utilities.add_validation_error(
                        validation_errors, choice_field[0], error_message
                    )
            # > type 'QCM' rules
            # - QCM question must have len(answer_correct) equal to 1 ('a', 'b', 'c' or 'd')
            if self.type == constants.QUESTION_TYPE_QCM:
                if self.answer_correct not in constants.QUESTION_TYPE_QCM_CHOICE_LIST:
                    error_message = f"Valeur : '{self.answer_correct}' doit être 'a', 'b', 'c' ou 'd'. Car type 'QCM'. Question {self.id}"  # noqa
                    validation_errors = utilities.add_validation_error(
                        validation_errors, "answer_correct", error_message
                    )
            # > type 'QCM-RM' rules
            # - QCM-RM question must have len(answer_correct) larger than 1 and lower than 5
            if self.type == constants.QUESTION_TYPE_QCM_RM:
                if (len(self.answer_correct) < 1) or (len(self.answer_correct) > 4):
                    error_message = f"Valeur : '{self.answer_correct}' longueur doit être égale à 1, 2, 3 or 4 ('a', 'ab' ... 'abcd'). Car type 'QCM-RM'. Question {self.id}"  # noqa
                    validation_errors = utilities.add_validation_error(
                        validation_errors, "answer_correct", error_message
                    )
            # type 'VF' rules
            # - Vrai/Faux question must have answer_correct equal to 'a' or 'b'
            # - Vrai/Faux question must have has_ordered_answers checked
            if self.type == constants.QUESTION_TYPE_VF:
                if self.answer_correct not in constants.QUESTION_TYPE_VF_CHOICE_LIST:
                    error_message = f"Valeur : '{self.answer_correct}' doit être 'a' ou 'b'. Car type 'VF'. Question {self.id}"  # noqa
                    validation_errors = utilities.add_validation_error(
                        validation_errors, "answer_correct", error_message
                    )
                if not getattr(self, "has_ordered_answers"):
                    error_message = f"Valeur : '{self.has_ordered_answers}' doit être True. Car type 'VF'. Question {self.id}"  # noqa
                    validation_errors = utilities.add_validation_error(
                        validation_errors, "has_ordered_answers", error_message
                    )
        if bool(validation_errors):
            raise ValidationError(validation_errors)


def question_validate_fields(sender, instance, **kwargs):
    """
    Validation for fixtures
    The rest of the Question model validation is done in the save() --> full_clean() call
    """
    # > if from fixtures, run clean & check that there is an id
    if kwargs.get("raw"):
        Question.clean(instance)
    if kwargs.get("raw") and not getattr(instance, "id"):
        raise ValidationError({"id": f"Valeur : 'empty'. " f"Question : {instance.id}"})


def question_create_agg_stat_instance(sender, instance, created, **kwargs):
    if created:
        if not hasattr(instance, "agg_stats"):
            from stats.models import QuestionAggStat

            QuestionAggStat.objects.create(question=instance)


models.signals.pre_save.connect(question_validate_fields, sender=Question)
models.signals.post_save.connect(question_create_agg_stat_instance, sender=Question)
