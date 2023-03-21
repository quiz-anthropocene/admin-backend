from datetime import date, timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from core import constants
from core.utils.utilities import truncate_with_ellipsis
from history.models import HistoryChangedFieldsAbstractModel
from questions.models import Question
from quizs.models import Quiz


class CommentQuerySet(models.QuerySet):
    def exclude_contributor_comments(self):
        return self.exclude(type=constants.COMMENT_TYPE_COMMENT_CONTRIBUTOR)

    def exclude_replies(self):
        return self.exclude(type=constants.COMMENT_TYPE_REPLY)

    def exclude_contributor_work(self):
        return self.exclude_contributor_comments().exclude_replies()

    def only_replies(self):
        return self.filter(type=constants.COMMENT_TYPE_REPLY)

    def only_notes(self):
        return self.filter(type=constants.COMMENT_TYPE_COMMENT_CONTRIBUTOR)

    def exclude_errors(self):
        return self.exclude(type=constants.COMMENT_TYPE_ERROR_APP)

    def last_30_days(self):
        return self.filter(created__date__gte=(date.today() - timedelta(days=30)))

    def has_replies_contributor_comments(self):
        return (
            self.prefetch_related("replies")
            .filter(replies__type=constants.COMMENT_TYPE_COMMENT_CONTRIBUTOR)
            .distinct()
        )

    def has_replies_reply(self):
        return self.prefetch_related("replies").filter(replies__type=constants.COMMENT_TYPE_REPLY).distinct()

    def has_replies_contributor_work(self):
        return (
            self.prefetch_related("replies")
            .filter(replies__type__in=[constants.COMMENT_TYPE_COMMENT_CONTRIBUTOR, constants.COMMENT_TYPE_REPLY])
            .distinct()
        )

    def has_parent(self):
        return self.select_related("parent").filter(parent__isnull=False)


class Comment(models.Model):
    COMMENT_CHOICE_FIELDS = ["type", "status"]
    COMMENT_FK_FIELDS = ["question", "quiz", "author"]
    COMMENT_READONLY_FIELDS = ["parent", "created", "updated"]

    text = models.TextField(
        verbose_name=_("Text"),
        blank=False,
        help_text=_("A question, a comment…"),
    )
    description = models.TextField(verbose_name=_("Additional information"), blank=True)
    type = models.CharField(verbose_name=_("Type"), max_length=150, choices=constants.COMMENT_TYPE_CHOICES, blank=True)

    question = models.ForeignKey(
        verbose_name=_("Question"),
        to=Question,
        related_name="comments",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    quiz = models.ForeignKey(
        verbose_name=_("Quiz"), to=Quiz, related_name="comments", on_delete=models.CASCADE, null=True, blank=True
    )
    author = models.ForeignKey(
        verbose_name=_("Author"),
        to=settings.AUTH_USER_MODEL,
        related_name="comments",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    status = models.CharField(
        verbose_name=_("Status"),
        max_length=150,
        choices=constants.COMMENT_STATUS_CHOICES,
        # default=constants.COMMENT_STATUS_PENDING,
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

    history = HistoricalRecords(bases=[HistoryChangedFieldsAbstractModel])

    objects = CommentQuerySet.as_manager()

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return f"{truncate_with_ellipsis(self.text, 60)}"

    @property
    def get_author(self) -> str:
        return self.author or _("Anonymous user")

    @property
    def has_parent(self) -> bool:
        return self.parent is not None

    @property
    def has_parent_icon(self) -> str:
        if self.has_parent:
            return "✅"
        return ""

    @property
    def has_replies(self) -> bool:
        return self.replies.exists()

    @property
    def has_replies_reply(self) -> bool:
        return self.replies.only_replies().exists()

    @property
    def has_replies_reply_icon(self) -> str:
        if self.has_replies_reply:
            return "✅"
        return ""

    @property
    def replies_reply(self):
        return self.replies.only_replies()

    @property
    def replies_notes(self):
        return self.replies.only_notes()

    @property
    def processed(self) -> bool:
        if self.status in [constants.COMMENT_STATUS_NEW, constants.COMMENT_STATUS_PENDING]:
            return False
        return True

    @property
    def processed_icon(self) -> str:
        if self.status == constants.COMMENT_STATUS_NEW:
            return "❌"
        if self.status == constants.COMMENT_STATUS_PENDING:
            return "📝"
        return "✅"

    # Admin
    has_parent.fget.short_description = _("Parent")
    has_parent_icon.fget.short_description = _("Parent")
    has_replies_reply.fget.short_description = _("Answered")
    has_replies_reply_icon.fget.short_description = _("Answered")
