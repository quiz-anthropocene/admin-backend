from django.db import models
from django.db.models import Avg, Count
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from ckeditor.fields import RichTextField

from api import constants, utilities


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
    language = models.CharField(
        max_length=50,
        choices=zip(constants.LANGUAGE_CHOICE_LIST, constants.LANGUAGE_CHOICE_LIST,),
        default=constants.LANGUAGE_FRENCH,
        blank=False,
        help_text="La langue de la question",
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
    answer_audio = models.URLField(
        max_length=500, blank=True, help_text="Une explication audio"
    )
    answer_video = models.URLField(
        max_length=500, blank=True, help_text="Une explication vidéo"
    )
    answer_accessible_url = models.URLField(
        max_length=500, blank=True, help_text="Un lien pour aller plus loin"
    )
    answer_scientific_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="La source scientifique du chiffre (rapport)",
    )
    answer_reading_recommendation = models.TextField(
        blank=True, help_text="Un livre pour aller plus loin"
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
    def has_answer_audio(self):
        return len(self.answer_audio) > 0

    @property
    def has_answer_video(self):
        return len(self.answer_video) > 0

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
                ("language", "LANGUAGE_CHOICE_LIST"),
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
    name = models.CharField(max_length=50, blank=False, help_text="Le nom du quiz")
    slug = models.SlugField(max_length=50, unique=True, help_text="Le bout d'url du quiz")
    introduction = RichTextField(blank=True, help_text="Une description du quiz")
    conclusion = RichTextField(
        blank=True,
        help_text="Une conclusion du quiz et des pistes pour aller plus loin",
    )
    questions = models.ManyToManyField(
        Question,
        through="QuizQuestion",
        related_name="quizzes",
        help_text="Les questions du quiz",
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="quizzes",
        help_text="Un ou plusieurs tags rattaché au quiz",
    )
    difficulty_average = models.FloatField(
        default=0, help_text="La difficulté moyenne des questions"  # readonly
    )
    language = models.CharField(
        max_length=50,
        choices=zip(constants.LANGUAGE_CHOICE_LIST, constants.LANGUAGE_CHOICE_LIST,),
        default=constants.LANGUAGE_FRENCH,
        blank=False,
        help_text="La langue du quiz",
    )
    author = models.CharField(max_length=50, blank=True, help_text="L'auteur du quiz")
    image_background_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="Un lien vers une image pour illustrer le quiz",
    )
    has_audio = models.BooleanField(
        default=False, help_text="Le quiz a du contenu audio"
    )
    publish = models.BooleanField(
        default=False, help_text="Le quiz est prêt à être publié"
    )
    spotlight = models.BooleanField(default=False, help_text="Le quiz est mis en avant")
    relationships = models.ManyToManyField(
        "self",
        through="QuizRelationship",
        symmetrical=False,
        related_name="related_to",
        help_text="Les quizs similaires ou liés",
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

    def set_slug(self):
        """
        The slug field should be unique.
        TODO: manage conflicts (e.g. add uuid4 at the end)
        """
        if not self.id:
            if not self.slug:
                self.slug = slugify(self.name)

    def save(self, *args, **kwargs):
        self.full_clean()
        self.set_slug()
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
    def questions_difficulty_average(self):
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
    def answer_count_agg(self):
        return self.stats.count()

    @property
    def duration_average(self):
        if self.answer_count_agg:
            duration_seconds_avg_raw = self.stats.aggregate(Avg("duration_seconds"))
            duration_seconds_average_value = (
                round(duration_seconds_avg_raw["duration_seconds__avg"], 1)
                if duration_seconds_avg_raw["duration_seconds__avg"]
                else 0
            )
            return duration_seconds_average_value
        return 0

    @property
    def like_count_agg(self):
        return self.feedbacks.liked().count()

    @property
    def dislike_count_agg(self):
        return self.feedbacks.disliked().count()

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
    duration_average.fget.short_description = "Durée moyenne (en secondes)"
    like_count_agg.fget.short_description = "# Like"
    dislike_count_agg.fget.short_description = "# Dislike"

    def clean(self):
        # > only run on existing (Quiz query won't work on new quizzes)
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
                    raise ValidationError(
                        {
                            "questions": f"Un quiz 'published' doit comporter au moins 1 question. "
                            f"Quiz {self.id}"
                        }
                    )
            # > compute questions difficulty_average
            self.difficulty_average = self.questions_difficulty_average


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


models.signals.pre_save.connect(quiz_validate_fields, sender=Quiz)


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(blank=True, default=0)
    # timestamps
    created = models.DateField(
        auto_now_add=True, help_text="La date de création du lien"
    )
    updated = models.DateField(auto_now=True)

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
                if QuizQuestion.objects.filter(
                    quiz=self.quiz, order=self.order
                ).exists():
                    raise ValidationError({"order": "la valeur existe déjà"})
        if not self.order:  # 0 or None
            last_quiz_question = QuizQuestion.objects.filter(quiz=self.quiz).last()
            self.order = (last_quiz_question.order + 1) if last_quiz_question else 1


class QuizRelationship(models.Model):
    from_quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="from_quizs"
    )
    to_quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="to_quizs")
    status = models.CharField(
        max_length=50,
        choices=zip(
            constants.QUIZ_RELATIONSHIP_CHOICE_LIST,
            constants.QUIZ_RELATIONSHIP_CHOICE_LIST,
        ),
        help_text="Le type de relation entre les deux quizs",
    )
    created = models.DateField(
        auto_now_add=True, help_text="La date & heure de la création de la relation"
    )

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
                raise ValidationError(
                    {"to_quiz": "il y a déjà une relation avec ce quiz dans ce sens"}
                )
            # check there isn't any existing symmetrical relationships
            existing_symmetrical_relationships = QuizRelationship.objects.filter(
                from_quiz=self.to_quiz, to_quiz=self.from_quiz
            )
            if len(existing_symmetrical_relationships):
                raise ValidationError(
                    {
                        "to_quiz": "il y a déjà une relation avec ce quiz dans l'autre sens"
                    }
                )


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
