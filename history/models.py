from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.dispatch import receiver
from simple_history.signals import post_create_historical_record

from history.utilities import get_diff_between_two_history_records


HISTORY_CHANGED_FIELDS_TO_IGNORE = [
    # all models
    "id",
    "created",
    "updated",
    # flatten FK
    "category_string",  # Question model
    "author_string",  # Question & Quiz model
    "validator_string",  # Question model
    # django-simple-history
    "history_id",
    "history_date",
    "history_type",
    "history_change_reason",
    "history_user_id",
    "history_changed_fields",
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
        changed_fields = get_diff_between_two_history_records(
            history_instance, old_record=history_instance.prev_record, returns="changed_fields"
        )
    # create action (most likely) : create list manually
    else:
        model_fields = [field.name for field in sender._meta.fields if field.name]
        changed_fields = [k for k, v in history_instance.__dict__.items() if k in model_fields if v]
    # cleanup changed_fields
    changed_fields_cleaned = [
        field_name for field_name in changed_fields if field_name not in HISTORY_CHANGED_FIELDS_TO_IGNORE
    ]
    # assign & save
    history_instance.history_changed_fields = changed_fields_cleaned
    history_instance.save()
