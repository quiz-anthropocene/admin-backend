from django.db import models


class GlossaryItem(models.Model):
    name = models.CharField(verbose_name="Mot ou sigle", max_length=50, blank=False)
    name_alternatives = models.TextField(verbose_name="Noms alternatifs", blank=True)  # ArrayField
    definition_short = models.CharField(verbose_name="Définition (succinte)", max_length=150, blank=False)
    description = models.TextField(verbose_name="Description", blank=True)
    description_accessible_url = models.URLField(verbose_name="Lien pour aller plus loin", max_length=500, blank=True)
    # timestamps
    added = models.DateField(blank=True, null=True, help_text="La date d'ajout du mot")
    created = models.DateTimeField(verbose_name="Date de création", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Date de dernière modification", auto_now=True)

    class Meta:
        ordering = ["name"]

    #     constraints = [
    #         models.UniqueConstraint(fields=["name"], name="glossary_name_unique")
    #     ]

    def __str__(self):
        return f"{self.name}"
