from django.db import models


class GlossaryItem(models.Model):
    name = models.CharField(max_length=50, blank=False, help_text="Le mot ou sigle")
    name_alternatives = models.TextField(blank=True, help_text="Des noms alternatifs")  # ArrayField
    definition_short = models.CharField(max_length=150, blank=False, help_text="La definition succinte du mot")
    description = models.TextField(blank=True, help_text="Une description longue du mot")
    description_accessible_url = models.URLField(max_length=500, blank=True, help_text="Un lien pour aller plus loin")
    # timestamps
    added = models.DateField(blank=True, null=True, help_text="La date d'ajout du mot")
    created = models.DateField(auto_now_add=True, help_text="La date de création du mot")
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ["name"]

    #     constraints = [
    #         models.UniqueConstraint(fields=["name"], name="unique glossary name")
    #     ]

    def __str__(self):
        return f"{self.name}"
