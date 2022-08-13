from django.db import models


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
        ("WEEKLY_AGG_STAT", "Statistiques de la semaine"),
    )

    # user
    actor_id = models.IntegerField(verbose_name="ID de l'acteur", blank=True)
    actor_name = models.CharField(verbose_name="Nom de l'acteur", max_length=150, blank=True)

    # event
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
