from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(verbose_name="Nom", max_length=50, blank=False)
    name_long = models.CharField(verbose_name="Nom (version longue)", max_length=150, blank=False)
    description = RichTextField(verbose_name="Description", blank=True)
    created = models.DateField(verbose_name="Date de création", auto_now_add=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["pk"]
        constraints = [models.UniqueConstraint(fields=["name"], name="category_name_unique")]

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("categories:detail", kwargs={"pk": self.id})

    @property
    def question_count(self) -> int:
        return self.questions.count()

    @property
    def question_validated_count(self) -> int:
        return self.questions.validated().count()

    # Admin
    question_validated_count.fget.short_description = "Questions (validées)"
