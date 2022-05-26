from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.dispatch import receiver
from simple_history.signals import post_create_historical_record


HISTORY_CHANGED_FIELDS_TO_IGNORE = [
    # model
    "id",
    "created",
    "updated",
    # django-simple-history
    "history_id",
    "history_date",
    "history_type",
]


class HistoryChangedFieldsAbstractModel(models.Model):
    history_changed_fields = ArrayField(
        verbose_name="Champs modifiés", base_field=models.CharField(max_length=50), blank=True, default=list
    )

    class Meta:
        abstract = True


# Populate history_changed_fields
@receiver(post_create_historical_record)
def post_create_historical_record_callback(sender, **kwargs):
    history_instance = kwargs["history_instance"]
    # update action
    if history_instance.prev_record:
        delta = history_instance.diff_against(history_instance.prev_record)
        changed_fields = delta.changed_fields
    # create action (most likely) : create list manually
    else:
        model_fields = [
            field.name for field in sender._meta.fields if field.name not in HISTORY_CHANGED_FIELDS_TO_IGNORE
        ]
        changed_fields = [k for k, v in history_instance.__dict__.items() if k in model_fields if v]
    history_instance.history_changed_fields = changed_fields
    history_instance.save()
