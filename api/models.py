from datetime import date, timedelta

from django.db import models
from django.db.models import Avg, Sum, Count
from django.core.exceptions import ValidationError

from solo.models import SingletonModel
from ckeditor.fields import RichTextField

from api import constants
from api import utilities


class Configuration(SingletonModel):
    # basics
    application_name = models.CharField(
        max_length=255,
        default="Quiz de l'Anthropocène",
        help_text="Le nom de l'application",
    )
    application_tagline = models.CharField(
        max_length=255, help_text="La tagline de l'application",
    )
    application_about = RichTextField(blank=True, help_text="A propos de l'application")
    # links
    application_backend_url = models.URLField(
        max_length=500, blank=True, help_text="Le lien vers le backend de l'application"
    )
    application_frontend_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="Le lien vers le frontend de l'application",
    )
    # timestamps
    daily_stat_last_aggregated = models.DateTimeField(
        null=True,
        blank=True,
        help_text="La dernière fois qu'a été lancé le script de mise à jour des Daily Stats",  # noqa
    )
    notion_questions_scope_1_last_imported = models.DateTimeField(
        null=True,
        blank=True,
        help_text="La dernière fois que les questions (lot 1) ont été importées depuis Notion",  # noqa
    )
    notion_questions_scope_2_last_imported = models.DateTimeField(
        null=True,
        blank=True,
        help_text="La dernière fois que les questions (lot 2) ont été importées depuis Notion",  # noqa
    )
    notion_questions_scope_3_last_imported = models.DateTimeField(
        null=True,
        blank=True,
        help_text="La dernière fois que les questions (lot 3) ont été importées depuis Notion",  # noqa
    )
    notion_questions_scope_4_last_imported = models.DateTimeField(
        null=True,
        blank=True,
        help_text="La dernière fois que les questions (lot 4) ont été importées depuis Notion",  # noqa
    )
    github_last_exported = models.DateTimeField(
        null=True,
        blank=True,
        help_text="La dernière fois que la donnée a été exportée vers Github",  # noqa
    )
    notion_contributions_last_exported = models.DateTimeField(
        null=True,
        blank=True,
        help_text="La dernière fois que les contributions exportées vers Notion",  # noqa
    )

    def __str__(self):
        return "Configuration de l'application"

    class Meta:
        verbose_name = "Configuration de l'application"


class Category(models.Model):
    name = models.CharField(
        max_length=50, blank=False, help_text="Le nom de la catégorie"
    )
    name_long = models.CharField(
        max_length=150, blank=False, help_text="Le nom allongé de la catégorie"
    )
    description = RichTextField(blank=True, help_text="Une description de la catégorie")
    created = models.DateField(
        auto_now_add=True, help_text="La date de création de la catégorie"
    )

    class Meta:
        ordering = ["pk"]
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique category name")
        ]

    def __str__(self):
        return f"{self.name}"

    @property
    def question_count(self):
        return self.questions.validated().count()

    # Admin
    question_count.fget.short_description = "Questions (validées)"


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
    description = RichTextField(blank=True, help_text="Une description du tag")
    created = models.DateField(
        auto_now_add=True, help_text="La date de création du tag"
    )

    objects = TagManager()

    class Meta:
        ordering = ["pk"]
        constraints = [models.UniqueConstraint(fields=["name"], name="unique tag name")]

    def __str__(self):
        return f"{self.name}"

    @property
    def question_count(self):
        return self.questions.validated().count()

    @property
    def quiz_count(self):
        return self.quizzes.published().count()

    # Admin
    question_count.fget.short_description = "Questions (validées)"
    quiz_count.fget.short_description = "Quizs (publiés)"


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
        Category,
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
    answer_option_a = models.CharField(
        max_length=500, blank=True, help_text="La réponse a"
    )
    answer_option_b = models.CharField(
        max_length=500, blank=True, help_text="La réponse b"
    )
    answer_option_c = models.CharField(
        max_length=500, blank=True, help_text="La réponse c"
    )
    answer_option_d = models.CharField(
        max_length=500, blank=True, help_text="La réponse d"
    )
    answer_correct = models.CharField(
        max_length=50,
        choices=zip(
            constants.QUESTION_ANSWER_CHOICE_LIST,
            constants.QUESTION_ANSWER_CHOICE_LIST,
        ),
        blank=True,
        help_text="a, b, c ou d. ab, acd, abcd, etc si plusieurs réponses.",
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
    validation_status = models.CharField(
        max_length=150,
        choices=zip(
            constants.QUESTION_VALIDATION_STATUS_LIST,
            constants.QUESTION_VALIDATION_STATUS_LIST,
        ),
        default=constants.QUESTION_VALIDATION_STATUS_NEW,
        help_text="Le statut de la question dans le workflow de validation",
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

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return f"{self.id} - {self.category} - {self.text}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Question, self).save(*args, **kwargs)

    @property
    def tags_list(self):
        return list(self.tags.values_list("name", flat=True))

    @property
    def tags_list_string(self):
        return ", ".join(self.tags_list)

    @property
    def quizs_list(self):
        return list(self.quizzes.values_list("name", flat=True))

    @property
    def quizs_list_string(self):
        return ", ".join(self.quizs_list)

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
                error_message = f"Valeur : '{self.category}' n'est pas une catégorie valide. Question {self.id}"  # noqa
                validation_errors = utilities.add_validation_error(
                    validation_errors, "category", error_message
                )
            # > relation fields: "category" & "tags" ? no need
            # checks will be done automatically to validate the existence of the foreign key.
            # > fields with choices rules
            question_choice_fields = [
                ("type", "QUESTION_TYPE_CHOICE_LIST"),
                ("difficulty", "QUESTION_DIFFICULTY_CHOICE_LIST"),
                ("answer_correct", "QUESTION_ANSWER_CHOICE_LIST"),
                # ("validation_status", "QUESTION_VALIDATION_STATUS_LIST"),
            ]
            for choice_field in question_choice_fields:
                if getattr(self, choice_field[0]) not in getattr(
                    constants, choice_field[1]
                ):
                    error_message = f"Valeur : '{getattr(self, choice_field[0])}' n'est pas bonne. Car pas dans les choix proposés. Question {self.id}"  # noqa
                    validation_errors = utilities.add_validation_error(
                        validation_errors, choice_field[0], error_message
                    )
            # > type 'QCM' rules
            # - QCM question must have len(answer_correct) equal to 1 ('a', 'b', 'c' or 'd')
            if self.type == constants.QUESTION_TYPE_QCM:
                if len(self.answer_correct) != 1:
                    error_message = f"Valeur : '{self.answer_correct}' doit être 'a', 'b', 'c' ou 'd'. Car type 'QCM'. Question {self.id}"  # noqa
                    validation_errors = utilities.add_validation_error(
                        validation_errors, "answer_correct", error_message
                    )
            # > type 'QCM-RM' rules
            # - QCM-RM question must have len(answer_correct) larger than 1 and lower than 5
            if self.type == constants.QUESTION_TYPE_QCM_RM:
                if (len(self.answer_correct) < 2) or (len(self.answer_correct) > 4):
                    error_message = f"Valeur : '{self.answer_correct}' longueur doit être égale à 2, 3 or 4 ('ab' ... 'abcd'). Car type 'QCM-RM'. Question {self.id}"  # noqa
                    validation_errors = utilities.add_validation_error(
                        validation_errors, "answer_correct", error_message
                    )
            # type 'VF' rules
            # - Vrai/Faux question must have answer_correct equal to 'a' or 'b'
            # - Vrai/Faux question must have has_ordered_answers checked
            if self.type == constants.QUESTION_TYPE_VF:
                if self.answer_correct not in ["a", "b"]:
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


class QuestionAnswerEventQuerySet(models.QuerySet):
    def for_question(self, question_id):
        return self.filter(question=question_id)

    def from_quiz(self):
        return self.filter(source=constants.QUESTION_SOURCE_QUIZ)

    def agg_timeseries(self):
        queryset = self
        queryset = (
            queryset.extra(select={"day": "to_char(created, 'YYYY-MM-DD')"})
            .values("day")
            .annotate(y=Count("created"))
            .order_by("day")
        )
        return queryset


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

    objects = QuestionAnswerEventQuerySet.as_manager()


class QuestionFeedbackEventQuerySet(models.QuerySet):
    def for_question(self, question_id):
        return self.filter(question=question_id)

    def liked(self):
        return self.filter(choice=constants.FEEDBACK_LIKE)

    def disliked(self):
        return self.filter(choice=constants.FEEDBACK_DISLIKE)

    def from_quiz(self):
        return self.filter(source=constants.QUESTION_SOURCE_QUIZ)


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
        return self.filter(publish=True)

    def for_author(self, author):
        return self.filter(author=author)


class Quiz(models.Model):
    name = models.CharField(max_length=50, blank=False, help_text="Le nom du quiz")
    introduction = RichTextField(blank=True, help_text="Une description du quiz")
    conclusion = RichTextField(
        blank=True,
        help_text="Une conclusion du quiz et des pistes pour aller plus loin",
    )
    questions = models.ManyToManyField(
        Question, related_name="quizzes", help_text="Les questions du quiz"
    )
    difficulty_average = models.FloatField(
        default=0, help_text="La difficulté moyenne des questions"  # readonly
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="quizzes",
        help_text="Un ou plusieurs tags rattaché au quiz",
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
    # timestamps
    created = models.DateField(
        auto_now_add=True, help_text="La date de création du quiz"
    )
    updated = models.DateField(auto_now=True)

    objects = QuizQuerySet.as_manager()

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Quiz, self).save(*args, **kwargs)

    @property
    def question_count(self):
        return self.questions.count()

    @property
    def tags_list(self):
        return list(self.tags.values_list("name", flat=True))

    @property
    def tags_list_string(self):
        return ", ".join(self.tags_list)

    @property
    def questions_categories_list(self):
        return list(
            self.questions.order_by()
            .values_list("category__name", flat=True)
            .distinct()
        )  # .sort()

    @property
    def questions_categories_list_with_count(self):
        return list(
            self.questions.values("category__name")
            .annotate(count=Count("category__name"))
            .order_by("-count")
        )

    @property
    def questions_categories_list_with_count_string(self):
        # return ", ".join(self.questions_categories_list)
        return ", ".join(
            [
                f"{elem['category__name']} ({elem['count']})"
                for elem in self.questions_categories_list_with_count
            ]
        )

    @property
    def questions_tags_list(self):
        return list(
            self.questions.order_by().values_list("tags__name", flat=True).distinct()
        )

    @property
    def questions_tags_list_with_count(self):
        return list(
            self.questions.values("tags__name")
            .annotate(count=Count("tags__name"))
            .order_by("-count")
        )

    @property
    def questions_tags_list_with_count_string(self):
        # return ", ".join(self.questions_tags_list_with_count)
        return ", ".join(
            [
                f"{elem['tags__name']} ({elem['count']})"
                for elem in self.questions_tags_list_with_count
            ]
        )

    @property
    def questions_authors_list(self):
        return list(
            self.questions.order_by().values_list("author", flat=True).distinct()
        )

    @property
    def questions_authors_list_with_count(self):
        return list(
            self.questions.values("author")
            .annotate(count=Count("author"))
            .order_by("-count")
        )

    @property
    def questions_authors_list_with_count_string(self):
        # return ", ".join(self.questions_authors_list_with_count)
        return ", ".join(
            [
                f"{elem['author']} ({elem['count']})"
                for elem in self.questions_authors_list_with_count
            ]
        )

    @property
    def questions_not_validated_list(self):
        return list(self.questions.not_validated())

    @property
    def questions_not_validated_string(self):
        return "<br />".join([str(q) for q in self.questions_not_validated_list])

    @property
    def like_count_agg(self):
        return self.feedbacks.liked().count()

    @property
    def dislike_count_agg(self):
        return self.feedbacks.disliked().count()

    @property
    def answer_count_agg(self):
        return self.stats.count()

    # Admin
    tags_list_string.fget.short_description = "Tag(s)"
    questions_not_validated_string.fget.short_description = (
        "Questions pas encore validées"
    )
    questions_categories_list_with_count_string.fget.short_description = (
        "Questions catégorie(s)"
    )
    questions_tags_list_with_count_string.fget.short_description = "Questions tag(s)"
    questions_authors_list_with_count_string.fget.short_description = (
        "Questions author(s)"
    )
    answer_count_agg.fget.short_description = "# Rép"
    like_count_agg.fget.short_description = "# Like"
    dislike_count_agg.fget.short_description = "# Dislike"

    def clean(self):
        # > only run on existing and published quizzes (Quiz query won't work on new quizzes)
        if getattr(self, "id") and getattr(self, "publish"):
            # > questions rules (only works for *existing* quiz questions, see quiz_validate_m2m_fields for new questions)  # noqa
            quiz_questions = Quiz.objects.get(pk=self.id).questions
            # - must have at least 1 question
            if quiz_questions.count() < 1:
                raise ValidationError(
                    {
                        "questions": f"Un quiz 'published' doit comporter au moins 1 question. "
                        f"Quiz {self.id}"
                    }
                )
            # - questions must be validated
            quiz_questions_ids = quiz_questions.values_list("id", flat=True)
            quiz_questions_validated_ids = (
                Question.objects.filter(pk__in=quiz_questions_ids)
                .validated()
                .values_list("id", flat=True)
            )
            if len(list(quiz_questions_ids)) != len(list(quiz_questions_validated_ids)):
                raise ValidationError(
                    {
                        "questions": f"Toutes les questions doivent être validées. "
                        f"not_validated questions : {[el for el in list(quiz_questions_ids) if el not in list(quiz_questions_validated_ids)]}. "  # noqa
                        f"Quiz {self.id}"
                    }
                )


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


def quiz_validate_m2m_fields(sender, **kwargs):
    """
    Method to validate *new* Quiz m2m fields.
    see question_validate_fields
    """
    # only run on published quizzes
    if (
        getattr(kwargs["instance"], "publish")
        and kwargs["instance"]
        and (kwargs["action"] == "pre_add")
    ):
        # > relation fields: check that the quiz's questions are validated
        quiz_questions_validated_ids = (
            Question.objects.filter(pk__in=kwargs["pk_set"])
            .validated()
            .values_list("id", flat=True)
        )
        if len(kwargs["pk_set"]) != len(list(quiz_questions_validated_ids)):
            raise ValidationError(
                {
                    "questions": f"Quiz pre_save_m2m error. "
                    # f"Questions count: {len(kwargs['pk_set'])}. Questions validated count: {len(list(quiz_questions_validated_ids))}. "  # noqa
                    f"Toutes les questions doivent être validées. "  # noqa
                    f"not_validated questions: {[el for el in kwargs['pk_set'] if el not in list(quiz_questions_validated_ids)]}"  # noqa
                }
            )
    # update difficulty_average
    if kwargs["action"].startswith("post"):
        difficulty_average_agg = kwargs["instance"].questions.aggregate(
            Avg("difficulty")
        )
        difficulty_average_value = (
            difficulty_average_agg["difficulty__avg"] if difficulty_average_agg else 0
        )
        kwargs["instance"].difficulty_average = difficulty_average_value
        kwargs["instance"].save(
            update_fields=["difficulty_average"]
        )  # will call clean() again...


models.signals.pre_save.connect(quiz_validate_fields, sender=Quiz)
models.signals.m2m_changed.connect(
    quiz_validate_m2m_fields, sender=Quiz.questions.through
)


class QuizAnswerEventQuerySet(models.QuerySet):
    def for_quiz(self, quiz_id):
        return self.filter(quiz=quiz_id)

    def last_30_days(self):
        return self.filter(created__date__gte=(date.today() - timedelta(days=30)))

    def agg_timeseries(self, scale="day"):
        queryset = self
        # scale
        if scale in ["day", "week"]:
            queryset = (
                queryset.extra(select={"day": "to_char(created, 'YYYY-MM-DD')"})
                .values("day")
                .annotate(y=Count("created"))
                .order_by("day")
            )
            if scale == "week":
                return utilities.aggregate_timeseries_by_week(queryset)

        if scale == "month":
            queryset = (
                queryset.extra(select={"day": "to_char(created, 'YYYY-MM-01')"})
                .values("day")
                .annotate(y=Count("created"))
                .order_by("day")
            )

        return queryset


class QuizAnswerEvent(models.Model):
    quiz = models.ForeignKey(
        Quiz, null=True, on_delete=models.CASCADE, related_name="stats"
    )
    # Why do we store the value instead of retrieving quiz.question_count ?
    # Because the value can change (adding or removing questions from a quiz)
    question_count = models.IntegerField(
        default=0, editable=False, help_text="La nombre de questions du quiz",
    )
    answer_success_count = models.IntegerField(
        default=0,
        editable=False,
        help_text="La nombre de réponses correctes trouvées par l'internaute",
    )
    created = models.DateTimeField(
        auto_now_add=True, help_text="La date & heure de la réponse"
    )

    objects = QuizAnswerEventQuerySet.as_manager()


class QuizFeedbackEventQuerySet(models.QuerySet):
    def liked(self):
        return self.filter(choice=constants.FEEDBACK_LIKE)

    def disliked(self):
        return self.filter(choice=constants.FEEDBACK_DISLIKE)

    def for_quiz(self, quiz_id):
        return self.filter(quiz=quiz_id)

    def agg_timeseries(self, scale="day"):
        queryset = self
        # scale
        if scale in ["day", "week"]:
            queryset = (
                queryset.extra(select={"day": "to_char(created, 'YYYY-MM-DD')"})
                .values("day")
                .annotate(y=Count("created"))
                .order_by("day")
            )
            if scale == "week":
                return utilities.aggregate_timeseries_by_week(queryset)

        if scale == "month":
            queryset = (
                queryset.extra(select={"day": "to_char(created, 'YYYY-MM-01')"})
                .values("day")
                .annotate(y=Count("created"))
                .order_by("day")
            )

        return queryset


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


class DailyStatManager(models.Manager):
    def agg_count(
        self,
        field="question_answer_count",
        since="total",
        week_or_month_iso_number=None,
    ):
        queryset = self
        # since
        if since not in constants.AGGREGATION_SINCE_CHOICE_LIST:
            raise ValueError(
                f"DailyStat agg_count: must be one of {constants.AGGREGATION_SINCE_CHOICE_LIST}"
            )
        if since == "last_30_days":
            queryset = queryset.filter(date__gte=(date.today() - timedelta(days=30)))
        if since == "month":
            queryset = queryset.filter(date__month=week_or_month_iso_number)
        elif since == "week":
            queryset = queryset.filter(date__week=week_or_month_iso_number)
        # field
        queryset = queryset.aggregate(Sum(field))[field + "__sum"]
        # returns None if aggregation is done on an empty queryset
        return queryset or 0

    def agg_timeseries(
        self,
        field="question_answer_count",
        scale=constants.AGGREGATION_SCALE_CHOICE_LIST[0],
        since_date=constants.AGGREGATION_SINCE_DATE_DEFAULT,
    ):
        """
        Output:
        [{'day': '2020-07-24', 'y': 1}, {'day': '2020-08-04', 'y': 13}]
        """
        queryset = self
        # since_date
        queryset = queryset.filter(date__gte=since_date)
        # scale
        if scale not in constants.AGGREGATION_SCALE_CHOICE_LIST:
            raise ValueError(
                f"DailyStat agg_timeseries: must be one of {constants.AGGREGATION_SCALE_CHOICE_LIST}"  # noqa
            )
        if scale in ["day", "week"]:
            queryset = (
                queryset.extra(
                    select={"day": "to_char(date, 'YYYY-MM-DD')", "y": field}
                )
                .values("day", "y")
                .order_by("day")
            )
            if scale == "week":
                return utilities.aggregate_timeseries_by_week(queryset)

        if scale == "month":
            queryset = (
                queryset.extra(
                    select={"day": "to_char(date, 'YYYY-MM-01')"}
                )  # use Trunc ?
                .values("day")
                .annotate(y=Sum(field))
                .order_by("day")
            )

        return queryset


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
    hour_split = models.JSONField(
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

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=["name"], name="unique glossary name")
    #     ]

    def __str__(self):
        return f"{self.name}"
