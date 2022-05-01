from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from core.fields import ChoiceArrayField
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
    def quiz_count(self) -> int:
        return self.quizs.count()

    @property
    def has_role_super_contributor(self) -> bool:
        return constants.USER_ROLE_SUPER_CONTRIBUTOR in self.roles

    @property
    def has_role_admin(self) -> bool:
        return constants.USER_ROLE_ADMINISTRATOR in self.roles
