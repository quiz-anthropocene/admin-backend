from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Exists, OuterRef, Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from core import constants
from core.fields import ChoiceArrayField
from core.utils import sendinblue
from history.models import HistoryChangedFieldsAbstractModel
from questions.models import Question
from quizs.models import QuizAuthor
from users import constants as user_constants


class UserQueryset(models.QuerySet):
    def all_contributors(self):
        return self.filter(
            roles__overlap=[
                user_constants.USER_ROLE_CONTRIBUTOR,
                user_constants.USER_ROLE_SUPER_CONTRIBUTOR,
                user_constants.USER_ROLE_ADMINISTRATOR,
            ]
        )

    def all_super_contributors(self):
        return self.filter(
            roles__overlap=[
                user_constants.USER_ROLE_SUPER_CONTRIBUTOR,
                user_constants.USER_ROLE_ADMINISTRATOR,
            ]
        )

    def all_administrators(self):
        return self.filter(
            roles__overlap=[
                user_constants.USER_ROLE_ADMINISTRATOR,
            ]
        )

    def has_question(self):
        return (
            self.prefetch_related("questions")
            .annotate(has_question=Exists(Question.objects.filter(author=OuterRef("pk"))))
            .filter(has_question=True)
        )

    def has_public_question(self):
        return (
            self.prefetch_related("questions")
            .annotate(has_public_question=Exists(Question.objects.filter(author=OuterRef("pk")).public()))
            .filter(has_public_question=True)
        )

    def has_quiz(self):
        return (
            self.prefetch_related("quizs")
            .annotate(has_quiz=Exists(QuizAuthor.objects.filter(author_id=OuterRef("pk"))))
            .filter(has_quiz=True)
        )

    def has_public_quiz(self):
        return (
            self.prefetch_related("quizs")
            .annotate(
                has_public_quiz=Exists(
                    QuizAuthor.objects.filter(author_id=OuterRef("pk")).exclude(
                        quiz__visibility=constants.VISIBILITY_PRIVATE
                    )
                )
            )
            .filter(has_public_quiz=True)
        )

    def has_public_content(self):
        # return self.has_public_question() | self.has_public_quiz()
        return (
            self.prefetch_related("questions", "quizs")
            .annotate(
                has_public_questions=Exists(Question.objects.filter(author=OuterRef("pk")).public()),
                has_public_quizs=Exists(
                    QuizAuthor.objects.filter(author_id=OuterRef("pk")).exclude(
                        quiz__visibility=constants.VISIBILITY_PRIVATE
                    )
                ),
            )
            .filter(Q(has_public_questions=True) | Q(has_public_quizs=True))
        )

    def has_user_card(self):
        return self.select_related("user_card").filter(user_card__isnull=False)

    def simple_search(self, value):
        search_fields = ["first_name", "last_name", "email"]
        conditions = Q()
        for field_name in search_fields:
            field_search = {f"{field_name}__icontains": value}
            conditions |= Q(**field_search)
        return self.filter(conditions)


class UserManager(BaseUserManager):
    def get_queryset(self):
        return UserQueryset(self.model, using=self._db)

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("Il manque l'adresse e-mail")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Un superuser doit avoir is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Un superuser doit avoir is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def all_contributors(self):
        return self.get_queryset().all_contributors()

    def all_super_contributors(self):
        return self.get_queryset().all_super_contributors()

    def all_administrators(self):
        return self.get_queryset().all_administrators()

    def has_question(self):
        return self.get_queryset().has_question()

    def has_public_question(self):
        return self.get_queryset().has_public_question()

    def has_quiz(self):
        return self.get_queryset().has_quiz()

    def has_public_quiz(self):
        return self.get_queryset().has_public_quiz()

    def has_public_content(self):
        return self.get_queryset().has_public_content()

    def has_user_card(self):
        return self.get_queryset().has_user_card()

    def simple_search(self, value):
        return self.get_queryset().simple_search(value)


class User(AbstractUser):
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    username = None
    email = models.EmailField(verbose_name=_("Email"), unique=True)
    first_name = models.CharField(verbose_name=_("First name"), max_length=150)
    last_name = models.CharField(verbose_name=_("Last name"), max_length=150)

    roles = ChoiceArrayField(
        verbose_name=_("Roles"),
        base_field=models.CharField(max_length=20, choices=user_constants.USER_ROLE_CHOICES),
        blank=True,
        default=list,
    )

    # is_active, is_staff, is_superuser
    # date_joined, last_login

    created = models.DateTimeField(verbose_name=_("Creation date"), default=timezone.now)
    updated = models.DateTimeField(verbose_name=_("Last update date"), auto_now=True)

    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.full_name

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def question_count(self) -> int:
        return self.questions.count()

    @property
    def question_public_count(self) -> int:
        return self.questions.public().count()

    @property
    def question_public_validated_count(self) -> int:
        return self.questions.public().validated().count()

    @property
    def has_question(self) -> bool:
        return self.question_count > 0

    @property
    def quiz_count(self) -> int:
        return self.quizs.count()

    @property
    def quiz_public_count(self) -> int:
        return self.quizs.public().count()

    @property
    def quiz_public_published_count(self) -> int:
        return self.quizs.public().published().count()

    @property
    def has_quiz(self) -> bool:
        return self.quiz_count > 0

    @property
    def has_user_card(self) -> bool:
        return hasattr(self, "user_card")

    @property
    def has_role_contributor(self) -> bool:
        ROLES_ALLOWED = [
            user_constants.USER_ROLE_ADMINISTRATOR,
            user_constants.USER_ROLE_SUPER_CONTRIBUTOR,
            user_constants.USER_ROLE_CONTRIBUTOR,
        ]
        return (len(self.roles) > 0) and any([role in ROLES_ALLOWED for role in self.roles])

    @property
    def has_role_super_contributor(self) -> bool:
        ROLES_ALLOWED = [user_constants.USER_ROLE_ADMINISTRATOR, user_constants.USER_ROLE_SUPER_CONTRIBUTOR]
        return (len(self.roles) > 0) and any([role in ROLES_ALLOWED for role in self.roles])

    @property
    def has_role_administrator(self) -> bool:
        ROLES_ALLOWED = [user_constants.USER_ROLE_ADMINISTRATOR]
        return (len(self.roles) > 0) and any([role in ROLES_ALLOWED for role in self.roles])

    def is_question_author(self, question) -> bool:
        return self == question.author

    def can_edit_question(self, question) -> bool:
        if question.is_private:
            return question.author == self
        return (question.author == self) or (self.has_role_super_contributor)

    def can_validate_question(self, question) -> bool:
        if question.is_private:
            return question.author == self
        return (question.author != self) and (self.has_role_administrator)

    def is_quiz_author(self, quiz) -> bool:
        return self in quiz.authors.all()

    def is_not_quiz_author(self, quiz) -> bool:
        return self not in quiz.authors.all()

    def can_edit_quiz(self, quiz) -> bool:
        if quiz.is_private:
            return self.is_quiz_author(quiz)
        return self.is_quiz_author(quiz) or (self.has_role_administrator)

    def can_publish_quiz(self, quiz) -> bool:
        if quiz.is_private:
            return self.is_quiz_author(quiz)
        return self.is_not_quiz_author(quiz) and (self.has_role_administrator)

    def can_edit_comment(self, comment) -> bool:
        return (comment.author == self) or (self.has_role_administrator)


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        if instance.has_role_contributor:
            sendinblue.add_to_contact_list(instance, list_id=settings.SIB_CONTRIBUTOR_LIST_ID)


class UserCard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="user_card")
    image_url = models.URLField(
        verbose_name=_("User image (link)"),
        max_length=500,
        blank=True,
    )
    short_biography = RichTextField(verbose_name=_("Short biography"), blank=True)
    quiz_relationship = RichTextField(verbose_name=_("Relationship with the Anthropocene Quiz"), blank=True)
    website_url = models.URLField(verbose_name=_("Website (link)"), max_length=500, blank=True)

    created = models.DateTimeField(verbose_name=_("Creation date"), default=timezone.now)
    updated = models.DateTimeField(verbose_name=_("Last update date"), auto_now=True)

    history = HistoricalRecords(bases=[HistoryChangedFieldsAbstractModel])

    class Meta:
        verbose_name = _("User card")
        verbose_name_plural = _("User cards")

    def __str__(self):
        return f"{self.user} >>> User card"

    @property
    def has_image_url(self) -> bool:
        return len(self.image_url) > 0

    @property
    def has_short_biography(self) -> bool:
        return len(self.short_biography) > 0

    @property
    def has_quiz_relationship(self) -> bool:
        return len(self.quiz_relationship) > 0

    @property
    def has_website_url(self) -> bool:
        return len(self.website_url) > 0
