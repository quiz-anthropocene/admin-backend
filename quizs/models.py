from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg, Count, Q
from django.db.models.functions import Concat
from django.db.models.signals import m2m_changed, post_delete, post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from simple_history.models import HistoricalRecords

from core import constants
from history.models import HistoryChangedFieldsAbstractModel
from questions.models import Question
from tags.models import Tag


class QuizQuerySet(models.QuerySet):
    def validated(self):
        return self.filter(validation_status=constants.VALIDATION_STATUS_OK)

    def not_validated(self):
        return self.exclude(validation_status=constants.VALIDATION_STATUS_OK)

    def published(self):
        return self.filter(publish=True)

    def spotlighted(self):
        return self.filter(spotlight=True)

    def public(self):
        return self.exclude(visibility=constants.VISIBILITY_PRIVATE)

    def have_audio(self):
        return self.filter(has_audio=True)

    def for_author(self, author):
        return self.filter(authors__in=[author])

    def simple_search(self, value):
        search_fields = ["name", "introduction", "conclusion"]
        conditions = Q()
        for field_name in search_fields:
            field_search = {f"{field_name}__icontains": value}
            conditions |= Q(**field_search)
        return self.filter(conditions)


class Quiz(models.Model):
    QUIZ_CHOICE_FIELDS = ["language", "validation_status", "visibility"]
    QUIZ_FK_FIELDS = []
    QUIZ_M2M_FIELDS = ["authors", "questions", "tags", "relationships"]
    QUIZ_RELATION_FIELDS = QUIZ_FK_FIELDS + QUIZ_M2M_FIELDS
    QUIZ_LIST_FIELDS = [
        "questions_categories_list",
        "questions_tags_list",
        "questions_authors_list",
    ]
    QUIZ_BOOLEAN_FIELDS = ["has_audio", "publish", "spotlight"]
    QUIZ_URL_FIELDS = []
    QUIZ_IMAGE_URL_FIELDS = ["image_background_url"]
    QUIZ_TIMESTAMP_FIELDS = ["created", "updated"]
    QUIZ_FLATTEN_FIELDS = [
        "tag_list",
        "question_list",
        "relationship_list",
        "author_list",
        "validator_string",
    ]
    QUIZ_READONLY_FIELDS = [
        "slug",
        "difficulty_average",
        "authors",
        "validator",
        "validation_date",
        "publish_date",
        "created",
        "updated",
    ] + QUIZ_FLATTEN_FIELDS

    name = models.CharField(verbose_name="Nom", max_length=50, blank=False)
    slug = models.SlugField(verbose_name="Fragment d'URL", max_length=50, unique=True)
    introduction = RichTextField(verbose_name="Introduction", blank=True)
    conclusion = RichTextField(
        verbose_name="Conclusion",
        blank=True,
        help_text="Inclure des pistes pour aller plus loin",
    )
    questions = models.ManyToManyField(
        verbose_name="Questions",
        to=Question,
        through="QuizQuestion",
        related_name="quizs",
    )
    tags = models.ManyToManyField(verbose_name="Tags", to=Tag, related_name="quizs", blank=True)
    difficulty_average = models.FloatField(verbose_name="Difficulté moyenne", default=0)  # readonly
    language = models.CharField(
        verbose_name="Langue",
        max_length=50,
        choices=constants.LANGUAGE_CHOICES,
        default=constants.LANGUAGE_FRENCH,
        blank=False,
    )
    authors = models.ManyToManyField(
        verbose_name="Auteurs",
        to=settings.AUTH_USER_MODEL,
        through="QuizAuthor",
        related_name="quizs",
        blank=True,
    )
    image_background_url = models.URLField(
        verbose_name="Lien vers une image pour illustrer le quiz",
        max_length=500,
        blank=True,
    )
    has_audio = models.BooleanField(verbose_name="Contenu audio ?", default=False)

    validation_status = models.CharField(
        verbose_name="Statut",
        max_length=150,
        choices=constants.VALIDATION_STATUS_CHOICES,
        default=constants.VALIDATION_STATUS_NEW,
    )
    validator = models.ForeignKey(
        verbose_name="Validateur",
        to=settings.AUTH_USER_MODEL,
        related_name="quizs_validated",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    validation_date = models.DateTimeField(verbose_name="Date de validation", blank=True, null=True)
    publish = models.BooleanField(verbose_name="Prêt à être publié ?", default=False)
    publish_date = models.DateTimeField(verbose_name="Date de publication", blank=True, null=True)

    spotlight = models.BooleanField(verbose_name="Mise en avant ?", default=False)
    visibility = models.CharField(
        verbose_name="Visibilité",
        max_length=50,
        choices=constants.VISIBILITY_CHOICES,
        default=constants.VISIBILITY_PUBLIC,
    )

    relationships = models.ManyToManyField(
        verbose_name="Les quizs similaires ou liés",
        to="self",
        through="QuizRelationship",
        symmetrical=False,
        related_name="related_to",
    )

    created = models.DateTimeField(verbose_name="Date de création", default=timezone.now)
    updated = models.DateTimeField(verbose_name="Date de dernière modification", auto_now=True)

    # flatten relations
    author_list = ArrayField(
        verbose_name="Auteurs", base_field=models.CharField(max_length=50), blank=True, default=list
    )
    tag_list = ArrayField(verbose_name="Tags", base_field=models.CharField(max_length=50), blank=True, default=list)
    question_list = ArrayField(
        verbose_name="Questions", base_field=models.PositiveIntegerField(), blank=True, default=list
    )
    relationship_list = ArrayField(
        verbose_name="Relations", base_field=models.CharField(max_length=50), blank=True, default=list
    )
    validator_string = models.CharField(verbose_name="Validateur", max_length=300, blank=True)

    history = HistoricalRecords(bases=[HistoryChangedFieldsAbstractModel])

    objects = QuizQuerySet.as_manager()

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizs"
        ordering = ["pk"]

    def __str__(self):
        return f"{self.name}"

    def set_slug(self):
        """
        The slug field should be unique.
        TODO: manage conflicts (e.g. add uuid4 at the end)
        """
        if not self.id:
            if not self.slug:
                self.slug = slugify(self.name)

    def set_difficulty_average(self):
        if self.id:
            self.difficulty_average = self.questions_difficulty_average

    def set_flatten_fields(self):
        # self.tag_list = self.tags_list  # see m2m_changed
        # self.question_list = self.questions_id_list_with_order  # see m2m_changed
        # self.relationship_list = self.relationships_list  # see m2m_changed
        self.validator_string = str(self.validator) if self.validator else ""

    def save(self, *args, **kwargs):
        self.set_slug()
        self.set_difficulty_average()
        # set_publication_date() in question/views.py
        self.set_flatten_fields()
        self.full_clean()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("quizs:detail", kwargs={"pk": self.id})

    @property
    def question_count(self) -> int:
        return self.questions.count()

    @property
    def questions_id_list(self) -> list:
        return list(self.questions.values_list("id", flat=True))

    @property
    def questions_id_list_with_order(self) -> list:
        return list(self.quizquestion_set.values_list("question_id", flat=True))

    @property
    def authors_list(self) -> list:
        return list(
            self.authors.annotate(fullname=Concat("first_name", models.Value(" "), "last_name")).values_list(
                "fullname", flat=True
            )
        )

    @property
    def authors_list_string(self) -> str:
        return ", ".join(self.authors_list)

    @property
    def tags_list(self) -> list:
        return list(self.tags.order_by("name").values_list("name", flat=True))

    @property
    def tags_list_string(self) -> str:
        return ", ".join(self.tags_list)

    @property
    def is_private(self) -> bool:
        return self.visibility == constants.VISIBILITY_PRIVATE

    @property
    def is_validated(self) -> bool:
        return self.validation_status == constants.VALIDATION_STATUS_OK

    @property
    def questions_categories_list(self) -> list:
        return list(self.questions.order_by().values_list("category__name", flat=True).distinct())  # .sort()

    @property
    def questions_categories_list_with_count(self) -> list:
        return list(self.questions.values("category__name").annotate(count=Count("category__name")).order_by("-count"))

    @property
    def questions_categories_list_with_count_string(self) -> str:
        # return ", ".join(self.questions_categories_list)
        return ", ".join(
            [f"{elem['category__name']} ({elem['count']})" for elem in self.questions_categories_list_with_count]
        )

    @property
    def questions_tags_list(self) -> list:
        return list(self.questions.order_by().values_list("tags__name", flat=True).distinct())

    @property
    def questions_tags_list_with_count(self) -> list:
        return list(self.questions.values("tags__name").annotate(count=Count("tags__name")).order_by("-count"))

    @property
    def questions_tags_list_with_count_string(self) -> str:
        # return ", ".join(self.questions_tags_list_with_count)
        return ", ".join([f"{elem['tags__name']} ({elem['count']})" for elem in self.questions_tags_list_with_count])

    @property
    def questions_authors_list(self) -> list:
        return list(self.questions.order_by().values_list("author", flat=True).distinct())

    @property
    def questions_authors_list_with_count(self) -> list:
        return list(self.questions.values("author").annotate(count=Count("author")).order_by("-count"))

    @property
    def questions_authors_list_with_count_string(self) -> str:
        # return ", ".join(self.questions_authors_list_with_count)
        return ", ".join([f"{elem['author']} ({elem['count']})" for elem in self.questions_authors_list_with_count])

    @property
    def questions_not_validated_list(self) -> list:
        return list(self.questions.not_validated())

    @property
    def questions_not_validated_string(self) -> str:
        return "<br />".join([str(q) for q in self.questions_not_validated_list])

    @property
    def questions_difficulty_average(self) -> int:
        questions_difficulty_avg_raw = self.questions.aggregate(Avg("difficulty"))
        questions_difficulty_average_value = (
            round(questions_difficulty_avg_raw["difficulty__avg"], 1)
            if questions_difficulty_avg_raw["difficulty__avg"]
            else 0
        )
        return questions_difficulty_average_value

    @property
    def relationships_all(self):
        return self.from_quizs.all() | self.to_quizs.all()

    @property
    def relationships_list(self) -> list:
        relationships_list = list()
        for rel in self.relationships_all:
            to_or_from_quiz_id = rel.to_quiz_id if rel.from_quiz_id == self.id else rel.from_quiz_id
            relationships_list.append(f"{to_or_from_quiz_id} ({rel.status_full(self.id)})")
        return relationships_list

    @property
    def answer_count_agg(self) -> int:
        return self.agg_stats.answer_count + self.stats.count()

    @property
    def duration_average_seconds(self) -> int:
        if self.answer_count_agg:
            duration_seconds_avg_raw = self.stats.exclude(duration_seconds=0).aggregate(Avg("duration_seconds"))
            duration_seconds_average_value = (
                round(duration_seconds_avg_raw["duration_seconds__avg"], 1)
                if duration_seconds_avg_raw["duration_seconds__avg"]
                else 0
            )
            return duration_seconds_average_value
        return 0

    @property
    def duration_average_minutes_string(self) -> str:
        if self.duration_average_seconds:
            duration_average_floor_minutes = self.duration_average_seconds // 60
            duration_average_floor_minutes_string = str(round(duration_average_floor_minutes))
            duration_average_remainder_seconds = self.duration_average_seconds % 60
            duration_average_remainder_seconds_string = str(round(duration_average_remainder_seconds))  # noqa
            if len(duration_average_remainder_seconds_string) == 1:
                duration_average_remainder_seconds_string = f"0{duration_average_remainder_seconds_string}"  # noqa
            return f"{duration_average_floor_minutes_string}min{duration_average_remainder_seconds_string}"  # noqa
        return ""

    @property
    def like_count_agg(self) -> int:
        return self.agg_stats.like_count + self.feedbacks.liked().count()

    @property
    def dislike_count_agg(self) -> int:
        return self.agg_stats.dislike_count + self.feedbacks.disliked().count()

    @property
    def contribution_count(self) -> int:
        return self.contributions.count()

    # Admin
    tags_list_string.fget.short_description = "Tags"
    authors_list_string.fget.short_description = "Auteurs"
    questions_not_validated_string.fget.short_description = "Questions pas encore validées"
    questions_categories_list_with_count_string.fget.short_description = "Questions catégories"
    questions_tags_list_with_count_string.fget.short_description = "Questions tags"
    questions_authors_list_with_count_string.fget.short_description = "Questions authors"
    answer_count_agg.fget.short_description = "# Rép"
    duration_average_seconds.fget.short_description = "Durée moyenne (en secondes)"
    duration_average_minutes_string.fget.short_description = "Durée moyenne (en minutes)"
    like_count_agg.fget.short_description = "# Like"
    dislike_count_agg.fget.short_description = "# Dislike"

    # TODO: commented because init_db_from_yaml raises ValidationError...
    # def clean(self):
    #     # > only run on existing (Quiz query won't work on new quizs)
    #     if getattr(self, "id"):
    #         # get quiz
    #         try:
    #             quiz = Quiz.objects.get(pk=self.id)
    #         except:  # noqa
    #             return
    #         # > basic question checks
    #         if getattr(self, "publish"):
    #             quiz_questions = quiz.questions
    #             # - must have at least 1 question
    #             if quiz_questions.count() < 1:
    #                 raise ValidationError({"questions": "Un quiz 'published' doit comporter au moins 1 question."})


@receiver(pre_save, sender=Quiz)
def quiz_validate_fields(sender, instance, **kwargs):
    """
    Validation for fixtures
    The rest of the Quiz model validation is done in the save() --> full_clean() call
    """
    # > if from fixtures, run clean & check that there is an id
    # if kwargs.get("raw"):
    #     Quiz.clean(instance) # won't work because Quiz doesn't exist yet, our custom clean() will fail  # noqa
    if kwargs.get("raw") and not getattr(instance, "id"):
        raise ValidationError({"id": f"Valeur : 'empty'. " f"Quiz: {instance}"})


@receiver(m2m_changed, sender=Quiz.tags.through)
def quiz_set_flatten_tag_list(sender, instance, action, **kwargs):
    if action in ("post_add", "post_remove", "post_clear"):
        instance.tag_list = instance.tags_list
        instance.save(update_fields=["tag_list"])


@receiver(post_save, sender=Quiz)
def quiz_create_agg_stat_instance(sender, instance, created, **kwargs):
    if created:
        if not hasattr(instance, "agg_stats"):
            from stats.models import QuizAggStat

            QuizAggStat.objects.create(quiz=instance)


class QuizQuestionQuerySet(models.QuerySet):
    def public(self):
        return self.exclude(quiz__visibility=constants.VISIBILITY_PRIVATE)


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(verbose_name="Quiz", to=Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(verbose_name="Question", to=Question, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(verbose_name="Ordre", blank=True, default=0)

    created = models.DateTimeField(verbose_name="Date de création", default=timezone.now)
    updated = models.DateTimeField(verbose_name="Date de dernière modification", auto_now=True)

    objects = QuizQuestionQuerySet.as_manager()

    class Meta:
        unique_together = [
            ["quiz", "question"],
            # ["quiz", "order"],  # empêche de réordonner simplement les questions
        ]
        ordering = ["quiz_id", "order"]

    def __str__(self):
        return f"Quiz {self.quiz.id} >>> Question {self.question.id} (#{self.order})"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self):
        """
        Rules on QuizQuestion
        - cannot add a new question with an existing order
        - if the order is 0 or None, increment from the biggest existing value
        - if the quiz is public, it cannot contain private questions
        """
        if not self.id:
            if self.order:
                if QuizQuestion.objects.filter(quiz=self.quiz, order=self.order).exists():
                    raise ValidationError({"order": "La valeur existe déjà"})
        if not self.order:  # 0 or None
            last_quiz_question = QuizQuestion.objects.filter(quiz=self.quiz).last()
            self.order = (last_quiz_question.order + 1) if last_quiz_question else 1
        if not self.quiz.is_private and self.question.is_private:
            raise ValidationError({"question": "Un quiz publique ne peut pas contenir de question privée"})


# @receiver(m2m_changed, sender=Quiz.questions.through)
@receiver(post_save, sender=QuizQuestion)
@receiver(post_delete, sender=QuizQuestion)
def quiz_set_flatten_question_list(sender, instance, **kwargs):
    instance.quiz.question_list = instance.quiz.questions_id_list_with_order
    instance.quiz.save()
    instance.question.quiz_list = instance.question.quizs_id_list
    instance.question.save()


class QuizRelationship(models.Model):
    from_quiz = models.ForeignKey(to=Quiz, on_delete=models.CASCADE, related_name="from_quizs")
    to_quiz = models.ForeignKey(to=Quiz, on_delete=models.CASCADE, related_name="to_quizs")
    status = models.CharField(
        verbose_name="Type de relation",
        max_length=50,
        choices=zip(
            constants.QUIZ_RELATIONSHIP_CHOICE_LIST,
            constants.QUIZ_RELATIONSHIP_CHOICE_LIST,
        ),
    )

    created = models.DateTimeField(verbose_name="Date de création", default=timezone.now)
    updated = models.DateTimeField(verbose_name="Date de dernière modification", auto_now=True)

    def __str__(self):
        return f"{self.from_quiz} >>> {self.status} >>> {self.to_quiz}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def status_full(self, quiz_id=None) -> str:
        if quiz_id and self.to_quiz_id == quiz_id:
            return "précédent"
        return self.status

    def clean(self):
        """
        Rules on QuizRelationship
        - cannot have the same from_quiz & to_quiz
        - status must be one of the choices
        - cannot have 2 relationships between 2 quizs
        - cannot have reverse ?
        """
        if self.status not in constants.QUIZ_RELATIONSHIP_CHOICE_LIST:
            raise ValidationError({"status": "doit être une valeur de la liste"})
        if self.from_quiz_id and self.to_quiz_id:
            if self.from_quiz_id == self.to_quiz_id:
                raise ValidationError({"to_quiz": "ne peut pas être le même quiz"})
            # check there isn't any existing relationships # status ?
            existing_identical_relationships = QuizRelationship.objects.filter(
                from_quiz=self.from_quiz, to_quiz=self.to_quiz
            )
            if len(existing_identical_relationships):
                raise ValidationError({"to_quiz": "il y a déjà une relation avec ce quiz dans ce sens"})
            # check there isn't any existing symmetrical relationships
            existing_symmetrical_relationships = QuizRelationship.objects.filter(
                from_quiz=self.to_quiz, to_quiz=self.from_quiz
            )
            if len(existing_symmetrical_relationships):
                raise ValidationError({"to_quiz": "il y a déjà une relation avec ce quiz dans l'autre sens"})


# @receiver(m2m_changed, sender=Quiz.relationships.through)
@receiver(post_save, sender=QuizRelationship)
@receiver(post_delete, sender=QuizRelationship)
def quiz_set_flatten_relationship_list(sender, instance, **kwargs):
    instance.from_quiz.relationship_list = instance.from_quiz.relationships_list
    instance.from_quiz.save()
    instance.to_quiz.relationship_list = instance.to_quiz.relationships_list
    instance.to_quiz.save()


class QuizAuthor(models.Model):
    quiz = models.ForeignKey(verbose_name="Quiz", to=Quiz, on_delete=models.CASCADE)
    author = models.ForeignKey(
        verbose_name="Auteur",
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    created = models.DateTimeField(verbose_name="Date de création", default=timezone.now)
    updated = models.DateTimeField(verbose_name="Date de dernière modification", auto_now=True)

    class Meta:
        unique_together = [
            ["quiz", "author"],
        ]

    def __str__(self):
        return f"Quiz {self.quiz.id} >>> Author {self.author.id}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


# called on QuizAuthor.objects.create() ; when editing the quiz in the Django Admin form
@receiver(post_save, sender=QuizAuthor)
@receiver(post_delete, sender=QuizAuthor)
def quiz_set_flatten_author_list(sender, instance, **kwargs):
    instance.quiz.author_list = instance.quiz.authors_list
    instance.quiz.save()


# called on quiz.authors.add() ; quiz.authors.set()
@receiver(m2m_changed, sender=Quiz.authors.through)
def quiz_set_flatten_author_list_m2m(sender, instance, action, **kwargs):
    if action in ("post_add", "post_remove", "post_clear"):
        instance.author_list = instance.authors_list
        instance.save(update_fields=["author_list"])
