from ckeditor.fields import RichTextField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg, Count
from django.urls import reverse
from django.utils.text import slugify
from simple_history.models import HistoricalRecords

from core import constants
from questions.models import Question
from tags.models import Tag


class QuizQuerySet(models.QuerySet):
    def published(self):
        return self.filter(publish=True)

    def spotlighted(self):
        return self.filter(spotlight=True)

    def have_audio(self):
        return self.filter(has_audio=True)

    def for_author(self, author):
        return self.filter(author=author)


class Quiz(models.Model):
    QUIZ_CHOICE_FIELDS = ["language"]
    QUIZ_FK_FIELDS = ["author"]
    QUIZ_M2M_FIELDS = ["questions", "tags", "relationships"]
    QUIZ_LIST_FIELDS = [
        "questions_categories_list",
        "questions_tags_list",
        "questions_authors_list",
    ]
    QUIZ_BOOLEAN_FIELDS = ["has_audio", "publish", "spotlight"]
    QUIZ_URL_FIELDS = []
    QUIZ_IMAGE_URL_FIELDS = ["image_background_url"]
    QUIZ_TIMESTAMP_FIELDS = ["created", "updated"]
    QUIZ_READONLY_FIELDS = ["slug", "difficulty_average", "author_old", "author", "created", "updated"]

    name = models.CharField(verbose_name="Nom", max_length=50, blank=False)
    slug = models.SlugField(verbose_name="Fragment d'URL", max_length=50, unique=True)
    introduction = RichTextField(verbose_name="Introduction", blank=True)
    conclusion = RichTextField(
        verbose_name="Conclusion",
        blank=True,
        help_text="Inclure des pistes pour aller plus loin",
    )
    questions = models.ManyToManyField(
        verbose_name="Les questions",
        to=Question,
        through="QuizQuestion",
        related_name="quizs",
    )
    tags = models.ManyToManyField(verbose_name="Tag(s)", to=Tag, related_name="quizs", blank=True)
    difficulty_average = models.FloatField(verbose_name="Difficulté moyenne", default=0)  # readonly
    language = models.CharField(
        verbose_name="Langue",
        max_length=50,
        choices=constants.LANGUAGE_CHOICES,
        default=constants.LANGUAGE_FRENCH,
        blank=False,
    )
    author_old = models.CharField(verbose_name="Auteur", max_length=50, blank=True)
    author = models.ForeignKey(
        verbose_name="Auteur",
        to=settings.AUTH_USER_MODEL,
        related_name="quizs",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    image_background_url = models.URLField(
        verbose_name="Lien vers une image pour illustrer le quiz",
        max_length=500,
        blank=True,
    )
    has_audio = models.BooleanField(verbose_name="Contenu audio ?", default=False)
    publish = models.BooleanField(verbose_name="Prêt à être publié ?", default=False)
    spotlight = models.BooleanField(verbose_name="Mise en avant ?", default=False)
    relationships = models.ManyToManyField(
        verbose_name="Les quizs similaires ou liés",
        to="self",
        through="QuizRelationship",
        symmetrical=False,
        related_name="related_to",
    )
    # timestamps
    created = models.DateTimeField(verbose_name="Date de création", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Date de dernière modification", auto_now=True)

    history = HistoricalRecords()

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

    def save(self, *args, **kwargs):
        self.set_slug()
        self.set_difficulty_average()
        self.full_clean()
        return super(Quiz, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("quizs:detail", kwargs={"pk": self.id})

    @property
    def question_count(self) -> int:
        return self.questions.count()

    @property
    def tags_list(self) -> list:
        return list(self.tags.values_list("name", flat=True))

    @property
    def tags_list_string(self) -> str:
        return ", ".join(self.tags_list)

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
    tags_list_string.fget.short_description = "Tag(s)"
    questions_not_validated_string.fget.short_description = "Questions pas encore validées"
    questions_categories_list_with_count_string.fget.short_description = "Questions catégorie(s)"
    questions_tags_list_with_count_string.fget.short_description = "Questions tag(s)"
    questions_authors_list_with_count_string.fget.short_description = "Questions author(s)"
    answer_count_agg.fget.short_description = "# Rép"
    duration_average_seconds.fget.short_description = "Durée moyenne (en secondes)"
    duration_average_minutes_string.fget.short_description = "Durée moyenne (en minutes)"
    like_count_agg.fget.short_description = "# Like"
    dislike_count_agg.fget.short_description = "# Dislike"

    def clean(self):
        # > only run on existing (Quiz query won't work on new quizs)
        if getattr(self, "id"):
            # get quiz
            try:
                quiz = Quiz.objects.get(pk=self.id)
            except:  # noqa
                return
            # > basic question checks
            if getattr(self, "publish"):
                quiz_questions = quiz.questions
                # - must have at least 1 question
                if quiz_questions.count() < 1:
                    raise ValidationError({"questions": "Un quiz 'published' doit comporter au moins 1 question."})


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


def quiz_create_agg_stat_instance(sender, instance, created, **kwargs):
    if created:
        if not hasattr(instance, "agg_stats"):
            from stats.models import QuizAggStat

            QuizAggStat.objects.create(quiz=instance)


models.signals.pre_save.connect(quiz_validate_fields, sender=Quiz)
models.signals.post_save.connect(quiz_create_agg_stat_instance, sender=Quiz)


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(verbose_name="Quiz", to=Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(verbose_name="Question", to=Question, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(verbose_name="Ordre", blank=True, default=0)
    # timestamps
    created = models.DateTimeField(verbose_name="Date de création", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Date de dernière modification", auto_now=True)

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
        return super(QuizQuestion, self).save(*args, **kwargs)

    def clean(self):
        """
        Rules on QuizQuestion
        - cannot add a new question with an existing order
        - if the order is 0 or None, increment from the biggest existing value
        """
        if not self.id:
            if self.order:
                if QuizQuestion.objects.filter(quiz=self.quiz, order=self.order).exists():
                    raise ValidationError({"order": "la valeur existe déjà"})
        if not self.order:  # 0 or None
            last_quiz_question = QuizQuestion.objects.filter(quiz=self.quiz).last()
            self.order = (last_quiz_question.order + 1) if last_quiz_question else 1


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
    created = models.DateTimeField(verbose_name="Date de création", auto_now_add=True)

    def __str__(self):
        return f"{self.from_quiz} >>> {self.status} >>> {self.to_quiz}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(QuizRelationship, self).save(*args, **kwargs)

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
