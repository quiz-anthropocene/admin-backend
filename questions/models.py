from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q, Sum
from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from core import constants
from core.templatetags.get_verbose_name import get_verbose_name
from core.utils import utilities
from history.models import HistoryChangedFieldsAbstractModel
from tags.models import Tag


class QuestionQuerySet(models.QuerySet):
    def validated(self):
        return self.filter(validation_status=constants.VALIDATION_STATUS_VALIDATED)

    def not_validated(self):
        return self.exclude(validation_status=constants.VALIDATION_STATUS_VALIDATED)

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
            "answer_choice_a",
            "answer_choice_b",
            "answer_choice_c",
            "answer_choice_d",
            "answer_explanation",
        ]
        # "answer_book_recommendation", "answer_image_url_text", "answer_extra_info"
        conditions = Q()
        for field_name in search_fields:
            field_search = {f"{field_name}__icontains": value}
            conditions |= Q(**field_search)
        return self.filter(conditions)

    def answer_count(self) -> int:
        return self.aggregate(answer_count=Sum("agg_stats__answer_count"))["answer_count"] or 0

    def answer_success_count(self) -> int:
        return self.aggregate(answer_success_count=Sum("agg_stats__answer_success_count"))["answer_success_count"] or 0

    def answer_success_count_ratio(self, decimal=0) -> int:
        answer_count = self.answer_count()
        if answer_count == 0:
            return 0
        return round(self.answer_success_count() / self.answer_count() * 100, decimal)

    def like_count(self) -> int:
        return self.aggregate(like_count=Sum("agg_stats__like_count"))["like_count"] or 0

    def dislike_count(self) -> int:
        return self.aggregate(dislike_count=Sum("agg_stats__dislike_count"))["dislike_count"] or 0


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
    QUESTION_BOOLEAN_FIELDS = ["has_ordered_answers", "author_certify_necessary_rights", "author_agree_commercial_use"]
    QUESTION_URL_FIELDS = [
        "answer_audio_url",
        "answer_video_url",
        "answer_source_accessible_url",
        "answer_source_scientific_url",
    ]
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

    text = models.TextField(verbose_name=_("Text"), blank=False, help_text=_("Keep it simple"))
    hint = models.TextField(
        verbose_name=_("Hint"), blank=True, help_text=_("Text that the user can decide to display to help him")
    )
    type = models.CharField(
        verbose_name=_("Type"),
        max_length=50,
        choices=constants.QUESTION_TYPE_CHOICES,
        default=constants.QUESTION_TYPE_QCM,
        blank=False,
    )
    category = models.ForeignKey(
        verbose_name=_("Category"),
        to="categories.Category",
        related_name="questions",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    tags = models.ManyToManyField(
        verbose_name=_("Tags"),
        to=Tag,
        related_name="questions",
        blank=True,
    )
    difficulty = models.IntegerField(
        verbose_name=_("Difficulty level"),
        choices=constants.QUESTION_DIFFICULTY_CHOICES,
        default=constants.QUESTION_DIFFICULTY_EASY,
        blank=False,
    )
    language = models.CharField(
        verbose_name=_("Language"),
        max_length=50,
        choices=constants.LANGUAGE_CHOICES,
        default=constants.LANGUAGE_FRENCH,
        blank=False,
    )
    answer_choice_a = models.CharField(verbose_name=_("Answer a"), max_length=500, blank=True)
    answer_choice_b = models.CharField(verbose_name=_("Answer b"), max_length=500, blank=True)
    answer_choice_c = models.CharField(verbose_name=_("Answer c"), max_length=500, blank=True)
    answer_choice_d = models.CharField(verbose_name=_("Answer d"), max_length=500, blank=True)
    answer_correct = models.CharField(
        verbose_name=_("The correct answer"),
        max_length=50,
        choices=constants.QUESTION_ANSWER_CHOICES,
        blank=True,
        help_text=f"a, b, c {_('or')} d (ab, acd, abcd… {_('if multiple answers')})",
    )
    has_ordered_answers = models.BooleanField(
        verbose_name=_("Ordered answers?"),
        default=True,
        help_text=_(
            "True if the answer choices should be displayed in this particular order (instead of being mixed up)"
        ),
    )
    answer_explanation = models.TextField(verbose_name=_("Answer explanation"), blank=True)
    answer_audio_url = models.URLField(verbose_name=_("Answer audio explanation (link)"), max_length=500, blank=True)
    answer_audio_url_text = models.CharField(
        verbose_name=_("Answer audio explanation (text to display)"),
        max_length=500,
        blank=True,
    )
    answer_video_url = models.URLField(verbose_name=_("Answer video explanation (link)"), max_length=500, blank=True)
    answer_video_url_text = models.CharField(
        verbose_name=_("Answer video explanation (text to display)"),
        max_length=500,
        blank=True,
    )
    answer_source_accessible_url = models.URLField(
        verbose_name=_("Answer accessible source (link)"), max_length=500, blank=True
    )
    answer_source_accessible_url_text = models.CharField(
        verbose_name=_("Answer accessible source (text to display)"),
        max_length=500,
        blank=True,
    )
    answer_source_scientific_url = models.URLField(
        verbose_name=_("Answer scientific source (link)"),
        max_length=500,
        blank=True,
        help_text=_("Report, scientific article…"),
    )
    answer_source_scientific_url_text = models.CharField(
        verbose_name=_("Answer scientific source (text to display)"),
        max_length=500,
        blank=True,
    )
    answer_book_recommendation = models.TextField(verbose_name=_("Answer reading recommandation"), blank=True)
    answer_image_url = models.URLField(
        verbose_name=_("Answer image (link)"),
        max_length=500,
        blank=True,
    )
    answer_image_url_text = models.TextField(
        verbose_name=_("Answer image (text to display)"),
        blank=True,
        help_text=_("Caption, translation, short explanation…"),
    )
    answer_extra_info = models.TextField(
        verbose_name=_("Answer extra info"),
        blank=True,
        help_text=_("Won't be displayed in the application"),
    )
    author = models.ForeignKey(
        verbose_name=_("Author"),
        to=settings.AUTH_USER_MODEL,
        related_name="questions",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    validation_status = models.CharField(
        verbose_name=_("Status"),
        max_length=150,
        choices=constants.VALIDATION_STATUS_CHOICES,
        default=constants.VALIDATION_STATUS_DRAFT,
    )
    validator = models.ForeignKey(
        verbose_name=_("Validator"),
        to=settings.AUTH_USER_MODEL,
        related_name="questions_validated",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    validation_date = models.DateTimeField(verbose_name=_("Validation date"), blank=True, null=True)

    visibility = models.CharField(
        verbose_name=_("Visibility"),
        max_length=50,
        choices=constants.VISIBILITY_CHOICES,
        default=constants.VISIBILITY_PUBLIC,
    )

    author_certify_necessary_rights = models.BooleanField(
        verbose_name=_("I certify that I have the necessary rights to publish and share this content"), default=True
    )
    author_agree_commercial_use = models.BooleanField(
        verbose_name=_("I agree to a possible commercial use by the association of this content"), default=True
    )

    created = models.DateTimeField(verbose_name=_("Creation date"), default=timezone.now)
    updated = models.DateTimeField(verbose_name=_("Last update date"), auto_now=True)

    # flatten relations
    category_string = models.CharField(verbose_name=_("Category"), max_length=50, blank=True)
    tag_list = ArrayField(verbose_name=_("Tags"), base_field=models.CharField(max_length=50), blank=True, default=list)
    quiz_list = ArrayField(verbose_name=_("Quizs"), base_field=models.PositiveIntegerField(), blank=True, default=list)
    author_string = models.CharField(verbose_name=_("Author"), max_length=300, blank=True)
    validator_string = models.CharField(verbose_name=_("Validator"), max_length=300, blank=True)

    history = HistoricalRecords(bases=[HistoryChangedFieldsAbstractModel])

    objects = QuestionQuerySet.as_manager()

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
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
        return super().save(*args, **kwargs)

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
    def has_answer_audio_url(self) -> bool:
        return len(self.answer_audio_url) > 0

    @property
    def has_answer_video_url(self) -> bool:
        return len(self.answer_video_url) > 0

    @property
    def has_answer_source_accessible_url(self) -> bool:
        return len(self.answer_source_accessible_url) > 0

    @property
    def has_answer_source_scientific_url(self) -> bool:
        return len(self.answer_source_scientific_url) > 0

    @property
    def has_answer_image_url(self) -> bool:
        return len(self.answer_image_url) > 0

    @property
    def is_private(self) -> bool:
        return self.visibility == constants.VISIBILITY_PRIVATE

    @property
    def is_validated(self) -> bool:
        return self.validation_status == constants.VALIDATION_STATUS_VALIDATED

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
    def comment_count(self) -> int:
        return self.comments.count()

    @property
    def comments_published(self):
        return self.comments.published()

    @property
    def success_rate(self):
        if self.answer_count_agg == 0:
            return "-"
        return f"{(self.answer_success_count_agg / self.answer_count_agg) * 100:.2f}%"

    # Admin
    tags_list_string.fget.short_description = _("Tags")
    quizs_list_string.fget.short_description = _("Quizs")
    answer_count_agg.fget.short_description = _("# Ans")
    answer_success_count_agg.fget.short_description = _("# Corr Ans")
    answer_success_rate.fget.short_description = _("% Corr Ans")
    like_count_agg.fget.short_description = _("# Like")
    dislike_count_agg.fget.short_description = _("# Dislike")

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
        if self.validation_status == constants.VALIDATION_STATUS_VALIDATED:
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
            if self.id:
                print("Question", self.id)
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
