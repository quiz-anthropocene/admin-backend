from django.db import models
from django.urls import reverse
from django.utils import timezone
from simple_history.models import HistoricalRecords

from history.models import HistoryChangedFieldsAbstractModel


class GlossaryItem(models.Model):
    GLOSSARY_URL_FIELDS = ["description_accessible_url"]
    GLOSSARY_ITEM_READONLY_FIELDS = ["created", "updated"]

    name = models.CharField(verbose_name="Mot ou sigle", max_length=50, blank=False)
    name_alternatives = models.TextField(verbose_name="Noms alternatifs", blank=True)  # ArrayField
    definition_short = models.CharField(verbose_name="Définition (succinte)", max_length=150, blank=False)
    description = models.TextField(verbose_name="Description", blank=True)
    description_accessible_url = models.URLField(verbose_name="Lien pour aller plus loin", max_length=500, blank=True)

    created = models.DateTimeField(verbose_name="Date de création", default=timezone.now)
    updated = models.DateTimeField(verbose_name="Date de dernière modification", auto_now=True)

    history = HistoricalRecords(bases=[HistoryChangedFieldsAbstractModel])

    class Meta:
        ordering = ["name"]
        constraints = [models.UniqueConstraint(fields=["name"], name="glossary_name_unique")]

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("glossary:detail", kwargs={"pk": self.id})
