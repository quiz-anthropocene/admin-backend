from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.utils import slack


"""
App to log the contributors activity

Current events logged:
- QUESTION: CREATED, VALIDATED
- QUIZ: CREATED, VALIDATED, PUBLISHED
- USER: CREATED
"""


class EventQuerySet(models.QuerySet):
    def display(self):
        # filters = Q(event_object_type="QUESTION") & Q(event_verb="CREATED")
        filters = Q(event_object_type="QUIZ") & Q(event_verb="PUBLISHED")
        filters |= Q(event_object_type="USER") & Q(event_verb="CREATED")
        return self.filter(filters)


class Event(models.Model):
    ACTIVITY_VERB_CHOICES = (
        ("CREATED", _("Created")),
        ("UPDATED", _("Updated")),
        ("VALIDATED", _("Validated")),
        ("PUBLISHED", _("Published")),
        ("DELETED", _("Deleted")),
        ("COMPUTED", _("Computed")),
    )
    EVENT_OBJECT_TYPE_CHOICES = (
        ("QUESTION", _("Question")),
        ("QUIZ", _("Quiz")),
        ("USER", _("Contributor")),
        ("WEEKLY_AGG_STAT", ("Weekly statistics")),
    )

    # user
    actor_id = models.IntegerField(verbose_name=_("Actor ID"), blank=True)
    actor_name = models.CharField(verbose_name=_("Actor name"), max_length=150, blank=True)

    # verb
    event_verb = models.CharField(
        verbose_name=_("Verb"),
        max_length=50,
        choices=ACTIVITY_VERB_CHOICES,
        blank=True,
    )

    # object
    event_object_id = models.IntegerField(verbose_name=_("Object ID"), blank=True)
    event_object_type = models.CharField(
        verbose_name=_("Object type"),
        max_length=50,
        choices=EVENT_OBJECT_TYPE_CHOICES,
        blank=True,
    )
    event_object_name = models.CharField(verbose_name=_("Object name"), max_length=150, blank=True)

    extra_data = models.JSONField(
        verbose_name=_("Additional data"),
        default=dict,
    )

    created = models.DateTimeField(verbose_name=_("Creation date"), default=timezone.now)

    objects = EventQuerySet.as_manager()

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    @property
    def get_event_object_admin_absolute_url(self):
        if self.event_object_type == "QUESTION":
            return reverse("questions:detail_view", kwargs={"pk": self.event_object_id})
        elif self.event_object_type == "QUIZ":
            return reverse("quizs:detail_view", kwargs={"pk": self.event_object_id})
        return ""

    @property
    def display_html(self) -> str:
        if self.event_object_type == "QUESTION":
            # Prénom Nom a créé la question 'Question'
            return self.display_question_with_admin_url_html
        elif self.event_object_type == "QUIZ":
            return self.display_quiz_with_admin_url_html
        elif self.event_object_type == "USER":
            return self.display_new_user_html

    @property
    def display_question_html(self) -> str:
        """
        💡 <i>Prénom Nom</i> created the question <strong>test</strong>
        """
        html_message = _("<i>{actor_name}</i> {event_verb} the question <strong>{question_name}</strong>").format(
            actor_name=self.actor_name,
            event_verb=self.get_event_verb_display().lower(),
            question_name=self.event_object_name,
        )
        return f"{self.display_event_emoji} {html_message}"

    @property
    def display_quiz_html(self) -> str:
        """
        💡 <i>Prénom Nom</i> created the quiz <strong>test</strong>
        """
        html_message = _("<i>{actor_name}</i> {event_verb} the quiz <strong>{quiz_name}</strong>").format(
            actor_name=self.actor_name,
            event_verb=self.get_event_verb_display().lower(),
            quiz_name=self.event_object_name,
        )
        return f"{self.display_event_emoji} {html_message}"

    @property
    def display_question_with_admin_url_html(self) -> str:
        """
        💡 <i>Prénom Nom</i> created the question <a href="/questions/<id>/view/">test</a>
        """
        html_message = _(
            '<i>{actor_name}</i> {event_verb} the question <a href="{question_admin_absolute_url}">{question_name}</a>'
        ).format(
            actor_name=self.actor_name,
            event_verb=self.get_event_verb_display().lower(),
            question_name=self.event_object_name,
            question_admin_absolute_url=self.get_event_object_admin_absolute_url,
        )
        return f"{self.display_event_emoji} {html_message}"

    @property
    def display_quiz_with_admin_url_html(self) -> str:
        """
        💡 <i>Prénom Nom</i> created the quiz <a href="/quizs/<id>/view/">test</a>
        """
        html_message = _(
            '<i>{actor_name}</i> {event_verb} the quiz <a href="{quiz_admin_absolute_url}">{quiz_name}</a>'
        ).format(
            actor_name=self.actor_name,
            event_verb=self.get_event_verb_display().lower(),
            quiz_name=self.event_object_name,
            quiz_admin_absolute_url=self.get_event_object_admin_absolute_url,
        )
        return f"{self.display_event_emoji} {html_message}"

    @property
    def display_new_user_html(self) -> str:
        html_message = _("New contributor! <i>{user_name}</i>").format(user_name=self.event_object_name)
        return f"{self.display_event_emoji} {html_message}"

    @property
    def display_event_emoji(self):
        if self.event_object_type in ["QUESTION", "QUIZ"]:
            if self.event_verb == "CREATED":
                return "💡"
            elif self.event_verb == "VALIDATED":
                return "✅"
            elif self.event_verb == "PUBLISHED":
                return "🚀"
        elif self.event_object_type in ["USER"]:
            if self.event_verb == "CREATED":
                return "🧑"


@receiver(post_save, sender=Event)
def send_event_to_slack(sender, instance, created, **kwargs):
    if created:
        slack.send_message_to_webhook(instance.display_html, webhook_url=settings.ACTIVITY_EVENT_WEBHOOK_URL)
