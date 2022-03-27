from ckeditor.fields import RichTextField
from django.db import models


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
    name = models.CharField(max_length=50, blank=False, help_text="Le nom du tag")
    description = RichTextField(blank=True, help_text="Une description du tag")
    created = models.DateField(auto_now_add=True, help_text="La date de création du tag")

    objects = TagManager()

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["pk"]
        constraints = [models.UniqueConstraint(fields=["name"], name="unique tag name")]

    def __str__(self):
        return f"{self.name}"

    @property
    def question_count(self) -> int:
        return self.questions.validated().count()

    @property
    def quiz_count(self) -> int:
        return self.quizs.published().count()

    # Admin
    question_count.fget.short_description = "Questions (validées)"
    quiz_count.fget.short_description = "Quizs (publiés)"
