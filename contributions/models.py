from datetime import date, timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core import constants
from questions.models import Question
from quizs.models import Quiz


class CommentQuerySet(models.QuerySet):
    def exclude_contributor_comments(self):
        return self.exclude(type=constants.CONTRIBUTION_TYPE_COMMENT_CONTRIBUTOR)

    def exclude_replies(self):
        return self.exclude(type=constants.CONTRIBUTION_TYPE_REPLY)

    def exclude_contributor_work(self):
        return self.exclude_contributor_comments().exclude_replies()

    def only_replies(self):
        return self.filter(type=constants.CONTRIBUTION_TYPE_REPLY)

    def exclude_errors(self):
        return self.exclude(type=constants.CONTRIBUTION_TYPE_ERROR_APP)

    def last_30_days(self):
        return self.filter(created__date__gte=(date.today() - timedelta(days=30)))


class Comment(models.Model):
    CONTRIBUTION_CHOICE_FIELDS = ["type", "status"]
    CONTRIBUTION_FK_FIELDS = ["question", "quiz", "author"]
    CONTRIBUTION_READONLY_FIELDS = ["parent", "created", "updated"]
    text = models.TextField(
        verbose_name=_("Text"),
        blank=False,
        help_text=_("A question, a comment…"),
    )
    description = models.TextField(verbose_name=_("Additional information"), blank=True)
    type = models.CharField(
        verbose_name=_("Type"), max_length=150, choices=constants.CONTRIBUTION_TYPE_CHOICES, blank=True
    )

    question = models.ForeignKey(
        verbose_name=_("Question"),
        to=Question,
        related_name="contributions",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    quiz = models.ForeignKey(
        verbose_name=_("Quiz"), to=Quiz, related_name="contributions", on_delete=models.CASCADE, null=True, blank=True
    )
    author = models.ForeignKey(
        verbose_name=_("Author"),
        to=settings.AUTH_USER_MODEL,
        related_name="contributions",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    status = models.CharField(
        verbose_name=_("Status"),
        max_length=150,
        choices=constants.CONTRIBUTION_STATUS_CHOICES,
        # default=constants.CONTRIBUTION_STATUS_PENDING,
        blank=True,
    )

    parent = models.ForeignKey(
        verbose_name=_("In reply to"),
        to="self",
        related_name="replies",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    created = models.DateTimeField(verbose_name=_("Creation date"), default=timezone.now)
    updated = models.DateTimeField(verbose_name=_("Last update date"), auto_now=True)

    objects = CommentQuerySet.as_manager()

    def __str__(self):
        return f"{self.text}"

    @property
    def get_author(self) -> str:
        return self.author or _("Anonymous user")

    def get_reply_type(self) -> str:
        return self.get_type_display().replace(_(" contributor"), "")

    @property
    def has_replies(self) -> bool:
        return self.replies.exists()

    @property
    def has_replies_reply(self) -> bool:
        return self.replies.only_replies().exists()

    @property
    def processed(self) -> bool:
        if self.status in [constants.CONTRIBUTION_STATUS_NEW, constants.CONTRIBUTION_STATUS_PENDING]:
            return False
        return True

    @property
    def processed_icon(self) -> str:
        if self.status == constants.CONTRIBUTION_STATUS_NEW:
            return "❌"
        if self.status == constants.CONTRIBUTION_STATUS_PENDING:
            return "📝"
        return "✅"
