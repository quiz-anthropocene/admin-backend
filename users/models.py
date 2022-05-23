from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Exists, OuterRef, Q

from core.fields import ChoiceArrayField
from questions.models import Question
from quizs.models import Quiz
from users import constants


class UserQueryset(models.QuerySet):
    def all_contributors(self):
        return self.filter(
            roles__overlap=[
                constants.USER_ROLE_CONTRIBUTOR,
                constants.USER_ROLE_SUPER_CONTRIBUTOR,
                constants.USER_ROLE_ADMINISTRATOR,
            ]
        )

    def all_super_contributors(self):
        return self.filter(
            roles__overlap=[
                constants.USER_ROLE_SUPER_CONTRIBUTOR,
                constants.USER_ROLE_ADMINISTRATOR,
            ]
        )

    def all_administrators(self):
        return self.filter(
            roles__overlap=[
                constants.USER_ROLE_ADMINISTRATOR,
            ]
        )

    def has_public_content(self):
        return (
            self.prefetch_related("questions", "quizs")
            .annotate(
                has_public_questions=Exists(Question.objects.filter(author=OuterRef("pk")).public()),
                has_public_quizs=Exists(Quiz.objects.filter(author=OuterRef("pk")).public()),
            )
            .filter(Q(has_public_questions=True) | Q(has_public_quizs=True))
        )


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

    def has_public_content(self):
        return self.get_queryset().has_public_content()


class User(AbstractUser):
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    username = None
    email = models.EmailField(verbose_name="Adresse e-mail", unique=True)
    first_name = models.CharField(verbose_name="Prénom", max_length=150)
    last_name = models.CharField(verbose_name="Nom", max_length=150)

    roles = ChoiceArrayField(
        verbose_name="Rôles",
        base_field=models.CharField(max_length=20, choices=constants.USER_ROLE_CHOICES),
        blank=True,
        default=list,
    )

    # is_active, is_staff, is_superuser
    # date_joined, last_login

    created = models.DateTimeField(verbose_name="Date de création", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Date de dernière modification", auto_now=True)

    objects = UserManager()

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return self.full_name

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def question_count(self) -> int:
        return self.questions.count()

    @property
    def question_public_validated_count(self) -> int:
        return self.questions.public().validated().count()

    @property
    def quiz_count(self) -> int:
        return self.quizs.count()

    @property
    def quiz_public_published_count(self) -> int:
        return self.quizs.public().published().count()

    @property
    def has_role_contributor(self) -> bool:
        ROLES_ALLOWED = [
            constants.USER_ROLE_ADMINISTRATOR,
            constants.USER_ROLE_SUPER_CONTRIBUTOR,
            constants.USER_ROLE_CONTRIBUTOR,
        ]
        return (len(self.roles) > 0) and any([role in ROLES_ALLOWED for role in self.roles])

    @property
    def has_role_super_contributor(self) -> bool:
        ROLES_ALLOWED = [constants.USER_ROLE_ADMINISTRATOR, constants.USER_ROLE_SUPER_CONTRIBUTOR]
        return (len(self.roles) > 0) and any([role in ROLES_ALLOWED for role in self.roles])

    @property
    def has_role_administrator(self) -> bool:
        ROLES_ALLOWED = [constants.USER_ROLE_ADMINISTRATOR]
        return (len(self.roles) > 0) and any([role in ROLES_ALLOWED for role in self.roles])

    def can_edit_question(self, question) -> bool:
        if question.is_private:
            return question.author == self
        return (question.author == self) or (self.has_role_super_contributor)

    def can_validate_question(self, question) -> bool:
        if question.is_private:
            return question.author == self
        return (question.author != self) and (self.has_role_administrator)

    def can_edit_quiz(self, quiz) -> bool:
        if quiz.is_private:
            return quiz.author == self
        return (quiz.author == self) or (self.has_role_administrator)

    def can_publish_quiz(self, quiz) -> bool:
        if quiz.is_private:
            return quiz.author == self
        return (quiz.author != self) and (self.has_role_administrator)
