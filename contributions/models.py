from datetime import date, timedelta

from django.conf import settings
from django.db import models

from core import constants
from questions.models import Question
from quizs.models import Quiz


class ContributionQuerySet(models.QuerySet):
    def exclude_errors(self):
        return self.exclude(type="erreur application")

    def last_30_days(self):
        return self.filter(created__date__gte=(date.today() - timedelta(days=30)))


class Contribution(models.Model):
    text = models.TextField(
        verbose_name="Texte",
        blank=False,
        help_text="Une question, un commentaire…",
    )
    description = models.TextField(verbose_name="Information supplémentaire", blank=True)
    type = models.CharField(
        verbose_name="Type",
        max_length=150,
        choices=constants.CONTRIBUTION_TYPE_CHOICES,
        blank=True,
    )

    question = models.ForeignKey(
        verbose_name="Question",
        to=Question,
        related_name="contributions",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    quiz = models.ForeignKey(
        verbose_name="Quiz", to=Quiz, related_name="contributions", on_delete=models.CASCADE, null=True, blank=True
    )
    author = models.ForeignKey(
        verbose_name="Auteur",
        to=settings.AUTH_USER_MODEL,
        related_name="contributions",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    created = models.DateTimeField(verbose_name="Date de création", auto_now_add=True)

    objects = ContributionQuerySet.as_manager()

    def __str__(self):
        return f"{self.text}"