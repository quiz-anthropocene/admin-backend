from ckeditor.fields import RichTextField
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, help_text="Le nom de la catégorie")
    name_long = models.CharField(max_length=150, blank=False, help_text="Le nom allongé de la catégorie")
    description = RichTextField(blank=True, help_text="Une description de la catégorie")
    created = models.DateField(auto_now_add=True, help_text="La date de création de la catégorie")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["pk"]
        constraints = [models.UniqueConstraint(fields=["name"], name="unique category name")]

    def __str__(self):
        return f"{self.name}"

    @property
    def question_count(self) -> int:
        return self.questions.validated().count()

    # Admin
    question_count.fget.short_description = "Questions (validées)"
