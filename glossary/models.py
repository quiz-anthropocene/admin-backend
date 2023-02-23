from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from core import constants
from history.models import HistoryChangedFieldsAbstractModel


class GlossaryItem(models.Model):
    GLOSSARY_ITEM_URL_FIELDS = ["description_accessible_url"]
    GLOSSARY_ITEM_READONLY_FIELDS = ["created", "updated"]

    name = models.CharField(verbose_name=_("Word or acronym"), max_length=50, blank=False)
    name_alternatives = models.TextField(verbose_name=_("Alternative names"), blank=True)  # ArrayField
    definition_short = models.CharField(verbose_name=_("Définition (short)"), max_length=150, blank=False)
    description = models.TextField(verbose_name=_("Description"), blank=True)
    description_accessible_url = models.URLField(
        verbose_name=_("Accessible source (link)"), max_length=500, blank=True
    )

    language = models.CharField(
        verbose_name=_("Language"),
        max_length=50,
        choices=constants.LANGUAGE_CHOICES,
        default=constants.LANGUAGE_FRENCH,
        blank=False,
    )

    created = models.DateTimeField(verbose_name=_("Creation date"), default=timezone.now)
    updated = models.DateTimeField(verbose_name=_("Last update date"), auto_now=True)

    history = HistoricalRecords(bases=[HistoryChangedFieldsAbstractModel])

    class Meta:
        ordering = ["name"]
        constraints = [models.UniqueConstraint(fields=["name"], name="glossary_name_unique")]

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("glossary:detail", kwargs={"pk": self.id})
