from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from simple_history.models import HistoricalRecords

from core import constants
from core.templatetags.get_verbose_name import get_verbose_name
from core.utils import utilities
from history.models import HistoryChangedFieldsAbstractModel
from tags.models import Tag


class QuestionQuerySet(models.QuerySet):
    def validated(self):
        return self.filter(validation_status=constants.VALIDATION_STATUS_OK)

    def not_validated(self):
        return self.exclude(validation_status=constants.VALIDATION_STATUS_OK)

    def public(self):
        return self.exclude(visibility=constants.VISIBILITY_PRIVATE)

    def for_category(self, category):
        return self.filter(category__name=category)

    def for_tag(self, tag):
        return self.filter(tags__name=tag)

    def for_author(self, author):
        return self.filter(author=author)

    def for_difficulty(self, difficulty):
        return self.filter(difficulty=difficulty)

    def public_or_by_author(self, author=None):
        if not author:
            return self.public()
        return self.filter(
            ~Q(visibility=constants.VISIBILITY_PRIVATE) | Q(author=author) & Q(visibility=constants.VISIBILITY_PRIVATE)
        )

    def simple_search(self, value):
        search_fields = [
            "text",
            "answer_option_a",
            "answer_option_b",
            "answer_option_c",
            "answer_option_d",
            "answer_explanation",
        ]
        # "answer_reading_recommendation", "answer_image_explanation", "answer_extra_info"
        conditions = Q()
        for field_name in search_fields:
            field_search = {f"{field_name}__icontains": value}
            conditions |= Q(**field_search)
        return self.filter(conditions)


class Question(models.Model):
    QUESTION_CHOICE_FIELDS = [
        "type",
        "difficulty",
        "language",
        "answer_correct",
        "validation_status",
        "visibility",
    ]
    QUESTION_FK_FIELDS = ["category", "author", "validator"]
    QUESTION_M2M_FIELDS = ["tags"]
    QUESTION_RELATION_FIELDS = QUESTION_FK_FIELDS + QUESTION_M2M_FIELDS
    QUESTION_BOOLEAN_FIELDS = ["has_ordered_answers"]
    QUESTION_URL_FIELDS = ["answer_audio", "answer_video", "answer_accessible_url", "answer_scientific_url"]
    QUESTION_IMAGE_URL_FIELDS = ["answer_image_url"]
    QUESTION_TIMESTAMP_FIELDS = ["created", "updated"]
    QUESTION_FLATTEN_FIELDS = ["category_string", "tag_list", "quiz_list", "author_string", "validator_string"]
    QUESTION_READONLY_FIELDS = [
        "author",
        "validator",
        "validation_status",
        "validation_date",
        "created",
        "updated",
    ] + QUESTION_FLATTEN_FIELDS

    text = models.TextField(
        verbose_name="Texte", blank=False, help_text="Rechercher la simplicité, faire des phrases courtes"
    )
    hint = models.TextField(
        verbose_name="Indice", blank=True, help_text="L'utilisateur pourra décider de l'afficher pour l'aider"
    )
    type = models.CharField(
        verbose_name="Type",
        max_length=50,
        choices=constants.QUESTION_TYPE_CHOICES,
        default=constants.QUESTION_TYPE_QCM,
        blank=False,
    )
    category = models.ForeignKey(
        verbose_name="Catégorie",
        to="categories.Category",
        related_name="questions",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    tags = models.ManyToManyField(
        verbose_name="Tags",
        to=Tag,
        related_name="questions",
        blank=True,
    )
    difficulty = models.IntegerField(
        verbose_name="Niveau de difficulté",
        choices=constants.QUESTION_DIFFICULTY_CHOICES,
        default=constants.QUESTION_DIFFICULTY_EASY,
        blank=False,
    )
    language = models.CharField(
        verbose_name="Langue",
        max_length=50,
        choices=constants.LANGUAGE_CHOICES,
        default=constants.LANGUAGE_FRENCH,
        blank=False,
    )
    answer_option_a = models.CharField(verbose_name="La réponse a", max_length=500, blank=True)
    answer_option_b = models.CharField(verbose_name="La réponse b", max_length=500, blank=True)
    answer_option_c = models.CharField(verbose_name="La réponse c", max_length=500, blank=True)
    answer_option_d = models.CharField(verbose_name="La réponse d", max_length=500, blank=True)
    answer_correct = models.CharField(
        verbose_name="La bonne réponse",
        max_length=50,
        choices=constants.QUESTION_ANSWER_CHOICES,
        blank=True,
        help_text="a, b, c ou d. ab, acd, abcd… si plusieurs réponses.",
    )
    has_ordered_answers = models.BooleanField(
        verbose_name="Réponses ordonnées ?",
        default=True,
        help_text="Les choix de réponse sont affichés dans cet ordre, et ne doivent pas être mélangés",
    )
    answer_explanation = models.TextField(verbose_name="Explication de texte de la bonne réponse", blank=True)
    answer_audio = models.URLField(verbose_name="Lien vers une explication audio", max_length=500, blank=True)
    answer_video = models.URLField(verbose_name="Lien vers une explication vidéo", max_length=500, blank=True)
    answer_accessible_url = models.URLField(
        verbose_name="Lien vers une source 'grand public'", max_length=500, blank=True
    )
    answer_accessible_url_text = models.CharField(
        verbose_name="Texte pour remplacer l'affichage du lien 'grand public'",
        max_length=500,
        blank=True,
    )
    answer_scientific_url = models.URLField(
        verbose_name="Lien vers une source 'scientifique'",
        max_length=500,
        blank=True,
        help_text="Rapport, article en anglais…",
    )
    answer_scientific_url_text = models.CharField(
        verbose_name="Texte pour remplacer l'affichage du lien 'scientifique'",
        max_length=500,
        blank=True,
    )
    answer_reading_recommendation = models.TextField(verbose_name="Un livre pour aller plus loin", blank=True)
    answer_image_url = models.URLField(
        verbose_name="Lien vers une image pour illustrer la réponse",
        max_length=500,
        blank=True,
    )
    answer_image_explanation = models.TextField(
        verbose_name="Texte explicatif pour l'image", blank=True, help_text="Légende, traduction, explication courte…"
    )
    answer_extra_info = models.TextField(
        verbose_name="Notes, commentaires et liens explicatifs additionels",
        blank=True,
        help_text="Ne s'affichera pas dans l'application",
    )
    author = models.ForeignKey(
        verbose_name="Auteur",
        to=settings.AUTH_USER_MODEL,
        related_name="questions",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    validator = models.ForeignKey(
        verbose_name="Validateur",
        to=settings.AUTH_USER_MODEL,
        related_name="questions_validated",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    validation_status = models.CharField(
        verbose_name="Statut",
        max_length=150,
        choices=constants.VALIDATION_STATUS_CHOICES,
        default=constants.VALIDATION_STATUS_NEW,
    )
    validation_date = models.DateTimeField(verbose_name="Date de validation", blank=True, null=True)

    visibility = models.CharField(
        verbose_name="Visibilité",
        max_length=50,
        choices=constants.VISIBILITY_CHOICES,
        default=constants.VISIBILITY_PUBLIC,
    )

    created = models.DateTimeField(verbose_name="Date de création", default=timezone.now)
    updated = models.DateTimeField(verbose_name="Date de dernière modification", auto_now=True)

    # flatten relations
    category_string = models.CharField(verbose_name="Catégorie", max_length=50, blank=True)
    tag_list = ArrayField(verbose_name="Tags", base_field=models.CharField(max_length=50), blank=True, default=list)
    quiz_list = ArrayField(verbose_name="Quizs", base_field=models.PositiveIntegerField(), blank=True, default=list)
    author_string = models.CharField(verbose_name="Auteur", max_length=300, blank=True)
    validator_string = models.CharField(verbose_name="Validateur", max_length=300, blank=True)

    history = HistoricalRecords(bases=[HistoryChangedFieldsAbstractModel])

    objects = QuestionQuerySet.as_manager()

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ["pk"]

    def __str__(self):
        return f"{self.id} - {self.text}"

    def set_flatten_fields(self):
        self.category_string = str(self.category) if self.category else ""
        # self.tag_list = self.tags_list  # see m2m_changed
        # self.quiz_list = self.quizs_id_list  # see m2m_changed (QuizQuestion)
        self.author_string = str(self.author) if self.author else ""
        self.validator_string = str(self.validator) if self.validator else ""

    def save(self, *args, **kwargs):
        # set_validator() in question/views.py
        self.set_flatten_fields()
        self.full_clean()
        return super(Question, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("questions:detail", kwargs={"pk": self.id})

    @property
    def tags_list(self) -> list:
        return list(self.tags.order_by("name").values_list("name", flat=True))

    @property
    def tags_list_string(self) -> str:
        return ", ".join(self.tags_list)

    @property
    def quizs_id_list(self) -> list:
        return list(self.quizs.values_list("id", flat=True))

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
    def is_private(self) -> bool:
        return self.visibility == constants.VISIBILITY_PRIVATE

    @property
    def is_validated(self) -> bool:
        return self.validation_status == constants.VALIDATION_STATUS_OK

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

    @property
    def quiz_count(self) -> int:
        return self.quizs.count()

    @property
    def contribution_count(self) -> int:
        return self.contributions.count()

    # Admin
    tags_list_string.fget.short_description = "Tags"
    quizs_list_string.fget.short_description = "Quizs"
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
        if self.validation_status == constants.VALIDATION_STATUS_OK:
            # > category rules
            if self.category is None:
                error_message = (
                    f"{get_verbose_name(self, 'category')} : '{self.category}' n'est pas une catégorie valide."
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
                # ("validation_status", "VALIDATION_STATUS_LIST"),
            ]
            for choice_field in question_choice_fields:
                if getattr(self, choice_field[0]) not in getattr(constants, choice_field[1]):
                    error_message = f"{get_verbose_name(self, choice_field[0])} : '{getattr(self, choice_field[0])}' n'est pas bonne (car pas dans les choix proposés)."  # noqa
                    validation_errors = utilities.add_validation_error(
                        validation_errors, choice_field[0], error_message
                    )
            # > type 'QCM' rules
            # - QCM question must have len(answer_correct) equal to 1 ('a', 'b', 'c' or 'd')
            if self.type == constants.QUESTION_TYPE_QCM:
                if self.answer_correct not in constants.QUESTION_TYPE_QCM_CHOICE_LIST:
                    error_message = f"{get_verbose_name(self, 'answer_correct')} : '{self.answer_correct}' doit être 'a', 'b', 'c' ou 'd' (car type 'QCM')."  # noqa
                    validation_errors = utilities.add_validation_error(
                        validation_errors, "answer_correct", error_message
                    )
            # > type 'QCM-RM' rules
            # - QCM-RM question must have len(answer_correct) larger than 1 and lower than 5
            if self.type == constants.QUESTION_TYPE_QCM_RM:
                if (len(self.answer_correct) < 1) or (len(self.answer_correct) > 4):
                    error_message = f"{get_verbose_name(self, 'answer_correct')} : '{self.answer_correct}' longueur doit être égale à 1, 2, 3 or 4 ('a', 'ab' ... 'abcd') (car type 'QCM-RM')."  # noqa
                    validation_errors = utilities.add_validation_error(
                        validation_errors, "answer_correct", error_message
                    )
            # type 'VF' rules
            # - Vrai/Faux question must have answer_correct equal to 'a' or 'b'
            # - Vrai/Faux question must have has_ordered_answers checked
            if self.type == constants.QUESTION_TYPE_VF:
                if self.answer_correct not in constants.QUESTION_TYPE_VF_CHOICE_LIST:
                    error_message = f"{get_verbose_name(self, 'answer_correct')} : '{self.answer_correct}' doit être 'a' ou 'b' (car type 'VF')."  # noqa
                    validation_errors = utilities.add_validation_error(
                        validation_errors, "answer_correct", error_message
                    )
                if not getattr(self, "has_ordered_answers"):
                    error_message = f"{get_verbose_name(self, 'has_ordered_answers')} : '{self.has_ordered_answers}' doit être True (car type 'VF')."  # noqa
                    validation_errors = utilities.add_validation_error(
                        validation_errors, "has_ordered_answers", error_message
                    )
        if bool(validation_errors):
            raise ValidationError(validation_errors)


@receiver(pre_save, sender=Question)
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


@receiver(m2m_changed, sender=Question.tags.through)
def question_set_flatten_tag_list(sender, instance, action, **kwargs):
    if action in ("post_add", "post_remove", "post_clear"):
        instance.tag_list = instance.tags_list
        instance.save(update_fields=["tag_list"])


@receiver(post_save, sender=Question)
def question_create_agg_stat_instance(sender, instance, created, **kwargs):
    if created:
        if not hasattr(instance, "agg_stats"):
            from stats.models import QuestionAggStat

            QuestionAggStat.objects.create(question=instance)
