from django.db import models
from django.db.models import Q


class EventQuerySet(models.QuerySet):
    def display(self):
        # filters = Q(event_object_type="QUESTION") & Q(event_verb="CREATED")
        filters = Q(event_object_type="QUIZ") & Q(event_verb="PUBLISHED")
        filters |= Q(event_object_type="USER") & Q(event_verb="CREATED")
        return self.filter(filters)


class Event(models.Model):
    ACTIVITY_VERB_CHOICES = (
        ("CREATED", "Créé"),
        ("UPDATED", "Mis à jour"),
        ("VALIDATED", "Validé"),
        ("PUBLISHED", "Publié"),
        ("DELETED", "Supprimé"),
        ("COMPUTED", "Calculé"),
    )
    EVENT_OBJECT_TYPE_CHOICES = (
        ("QUESTION", "Question"),
        ("QUIZ", "Quiz"),
        ("USER", "Contributeur"),
        ("WEEKLY_AGG_STAT", "Statistiques de la semaine"),
    )

    # user
    actor_id = models.IntegerField(verbose_name="ID de l'acteur", blank=True)
    actor_name = models.CharField(verbose_name="Nom de l'acteur", max_length=150, blank=True)

    # verb
    event_verb = models.CharField(
        verbose_name="Verbe",
        max_length=50,
        choices=ACTIVITY_VERB_CHOICES,
        blank=True,
    )

    # object
    event_object_id = models.IntegerField(verbose_name="ID de l'objet", blank=True)
    event_object_type = models.CharField(
        verbose_name="Type d'objet",
        max_length=50,
        choices=EVENT_OBJECT_TYPE_CHOICES,
        blank=True,
    )
    event_object_name = models.CharField(verbose_name="Nom de l'objet", max_length=150, blank=True)

    extra_data = models.JSONField(
        verbose_name="Données supplémentaires",
        default=dict,
    )

    created = models.DateTimeField(verbose_name="Date de création", auto_now_add=True)

    objects = EventQuerySet.as_manager()

    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"

    @property
    def display_full(self) -> str:
        if self.event_object_type in ["QUESTION", "QUIZ"]:
            return f"{self.display_event_emoji} <i>{self.actor_name}</i> a {self.get_event_verb_display().lower()} {self.display_event_object_type_prefix} {self.get_event_object_type_display().lower()} <strong>{self.event_object_name}</strong>"  # noqa
        elif self.event_object_type in ["USER"]:
            return f"{self.display_event_emoji} Nouveau contributeur ! <strong>{self.event_object_name}</strong>"

    @property
    def display_event_object_type_prefix(self) -> str:
        if self.event_object_type in ["QUESTION"]:
            return "la"
        return "le"

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
