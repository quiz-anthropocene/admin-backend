from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse


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
    name = models.CharField(verbose_name="Nom", max_length=50, blank=False)
    description = RichTextField(verbose_name="Description", blank=True)
    created = models.DateField(verbose_name="Date de création", auto_now_add=True)

    objects = TagManager()

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
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
    def question_validated_count(self) -> int:
        return self.questions.validated().count()

    @property
    def quiz_count(self) -> int:
        return self.quizs.count()

    @property
    def quiz_published_count(self) -> int:
        return self.quizs.published().count()

    # Admin
    question_validated_count.fget.short_description = "Questions (validées)"
    quiz_published_count.fget.short_description = "Quizs (publiés)"
