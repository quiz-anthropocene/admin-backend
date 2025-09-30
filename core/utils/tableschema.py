import json

from django.db import models


TYPE_MAPPING = {
    "AutoField": "integer",
    "BigAutoField": "integer",
    "BigIntegerField": "integer",
    "BinaryField": "string",
    "BooleanField": "boolean",
    "CharField": "string",
    "DateField": "date",
    "DateTimeField": "datetime",
    "DecimalField": "number",
    "DurationField": "string",
    "EmailField": "string",
    "FileField": "string",
    "FilePathField": "string",
    "FloatField": "number",
    "IntegerField": "integer",
    "GenericIPAddressField": "string",
    "NullBooleanField": "boolean",
    "PositiveIntegerField": "integer",
    "PositiveSmallIntegerField": "integer",
    "SlugField": "string",
    "SmallIntegerField": "integer",
    "TextField": "string",
    "TimeField": "time",
    "URLField": "string",
    "UUIDField": "string",
}


def generate_schema_from_model(model, exclude_fields=[]):
    """
    Generate a table schema from a Django model.
    The schema is a list of dictionaries, each representing a field in the model.
    Each dictionary contains:
    - name: the name of the field
    - type: the type of the field (CharField, IntegerField, etc.)
    - required: whether the field is required (not null and not blank)
    - choices: if the field has choices, a list of possible values
    """
    schema_name = f"schema-{model._meta.verbose_name_plural.lower()}"
    schema_filename = f"{schema_name}.json"
    schema = {
        "$schema": "https://frictionlessdata.io/schemas/table-schema.json",
        "encoding": "utf-8",
        "fields": [],
        "homepage": "https://github.com/quizanthropocene",
        "name": schema_name,
        "path": f"https://raw.githubusercontent.com/quizanthropocene/admin-backend/refs/heads/master/data/{schema_filename}",  # noqa
    }

    for field in model._meta.get_fields():
        # skip excluded fields
        if field.name in exclude_fields:
            continue
        # skip auto fields
        if isinstance(field, models.AutoField):
            continue
        # skip FK & M2M fields
        if field.is_relation:
            continue
        field_info = {
            "name": field.name,
            "type": TYPE_MAPPING.get(field.get_internal_type(), "string"),
            "required": not (field.null or field.blank),
        }
        if hasattr(field, "choices") and field.choices:
            field_info["choices"] = [choice[0] for choice in field.choices]
        schema["fields"].append(field_info)

    with open(f"data/{schema_filename}", "w", encoding="utf-8") as f:
        json.dump(schema, f, ensure_ascii=False, indent=4)
