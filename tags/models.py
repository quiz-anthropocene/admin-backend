from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TagManager(models.Manager):
    def get_ids_from_name_list(self, tag_name_list: list):
        tag_ids = []
        # Tag.objects.filter(name__in=tags_split) # ignores new tags
        for tag_name in tag_name_list:
            # tag, created = Tag.objects.get_or_create(name=tag_string)
            try:
                tag = Tag.objects.get(name=tag_name.strip())
            except Exception as e:
                raise type(e)(f"{tag_name}")
            tag_ids.append(tag.id)
        tag_ids.sort()
        return tag_ids


class Tag(models.Model):
    TAG_TIMESTAMP_FIELDS = ["created", "updated"]

    name = models.CharField(verbose_name=_("Name"), max_length=50, blank=False)
    description = RichTextField(verbose_name=_("Description"), blank=True)

    created = models.DateTimeField(verbose_name=_("Creation date"), default=timezone.now)
    updated = models.DateTimeField(verbose_name=_("Last update date"), auto_now=True)

    objects = TagManager()

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        ordering = ["pk"]
        constraints = [models.UniqueConstraint(fields=["name"], name="tag_name_unique")]

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("tags:detail", kwargs={"pk": self.id})

    @property
    def question_count(self) -> int:
        return self.questions.count()

    @property
    def question_public_validated_count(self) -> int:
        return self.questions.public().validated().count()

    @property
    def quiz_count(self) -> int:
        return self.quizs.count()

    @property
    def quiz_public_published_count(self) -> int:
        return self.quizs.public().published().count()

    # Admin
    question_public_validated_count.fget.short_description = _("Questions (public & validated)")
    quiz_public_published_count.fget.short_description = _("Quizs (public & published)")
