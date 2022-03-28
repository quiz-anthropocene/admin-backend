from datetime import date, timedelta

from django.db import models

from core import constants


class ContributionQuerySet(models.QuerySet):
    def last_30_days(self):
        return self.filter(created__date__gte=(date.today() - timedelta(days=30)))


class Contribution(models.Model):
    text = models.TextField(
        blank=False,
        help_text="La contribution de l'utilisateur (une question ou un commentaire)",
    )
    description = models.TextField(help_text="Informations supplémentaires sur la contribution (réponse, lien, ...)")
    type = models.CharField(
        max_length=150,
        choices=zip(
            constants.CONTRIBUTION_TYPE_LIST,
            constants.CONTRIBUTION_TYPE_LIST,
        ),
        blank=True,
        help_text="Le type de contribution",
    )
    created = models.DateTimeField(auto_now_add=True, help_text="La date & heure de la contribution")

    objects = ContributionQuerySet.as_manager()

    def __str__(self):
        return f"{self.text}"
