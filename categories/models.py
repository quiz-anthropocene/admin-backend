from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    CATEGORY_TIMESTAMP_FIELDS = ["created", "updated"]

    name = models.CharField(verbose_name=_("Name"), max_length=50, blank=False)
    name_long = models.CharField(verbose_name=_("Name (long version)"), max_length=150, blank=False)
    description = RichTextField(verbose_name=_("Description"), blank=True)

    created = models.DateTimeField(verbose_name=_("Creation date"), default=timezone.now)
    updated = models.DateTimeField(verbose_name=_("Last update date"), auto_now=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
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
    def question_public_validated_count(self) -> int:
        return self.questions.public().validated().count()

    # Admin
    question_public_validated_count.fget.short_description = _("Questions (public & validated)")
