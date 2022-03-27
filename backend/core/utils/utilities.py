import re

import yaml
from django.apps import apps
from django.core import serializers


def serialize_queryset_to_yaml(queryset, flat=False, stream=None):
    if not flat:
        return serializers.serialize("yaml", list(queryset), allow_unicode=True, stream=stream)
    serialized = serializers.serialize("yaml", list(queryset), allow_unicode=True)
    serialized = yaml.safe_load(serialized)
    serialized_flat = []
    # flatten list
    for item in serialized:
        # keep only fields, add new key 'id' to the top
        item_flat = {**{"id": item["pk"]}, **item["fields"]}
        serialized_flat.append(item_flat)
    return yaml.safe_dump(
        serialized_flat,
        allow_unicode=True,
        sort_keys=False,
        stream=stream,
    )


def serialize_model_to_yaml(app_label, model_label, flat=False, stream=None):
    model = apps.get_app_config(app_label).get_model(model_label)
    queryset = model.objects.all().order_by("pk")
    return serialize_queryset_to_yaml(queryset, flat=flat, stream=stream)


def serialize_queryset_to_json(queryset, stream=None):
    return serializers.serialize("json", list(queryset), ensure_ascii=False, stream=stream)


def serialize_model_to_json(app_label, model_label, stream=None):
    model = apps.get_app_config(app_label).get_model(model_label)
    queryset = model.objects.all().order_by("pk")
    return serialize_queryset_to_json(queryset, stream=stream)


def load_model_data_to_db(model, data):
    """
    translate ids to FK & M2M
    - FK: category
    - M2M: tags, questions
    """
    for index, item in enumerate(data):
        tag_ids = []
        question_ids = []
        # quiz_ids = []
        # FK
        if "category" in item:
            item["category_id"] = item["category"]
            del item["category"]
        if "quiz" in item:
            item["quiz_id"] = item["quiz"]
            del item["quiz"]
        if "question" in item:
            item["question_id"] = item["question"]
            del item["question"]
        if "from_quiz" in item:
            item["from_quiz_id"] = item["from_quiz"]
            del item["from_quiz"]
        if "to_quiz" in item:
            item["to_quiz_id"] = item["to_quiz"]
            del item["to_quiz"]
        # M2M
        if "tags" in item:
            tag_ids = item["tags"]
            del item["tags"]
        if "questions" in item:
            question_ids = item["questions"]
            del item["questions"]
        instance = model.objects.create(**item)
        if len(tag_ids):
            instance.tags.set(tag_ids)
        if len(question_ids):
            instance.questions.set(question_ids)


def add_validation_error(dict, key, value):
    if key not in dict:
        dict[key] = value
    else:
        if type(dict[key]) == list:
            dict[key] += [value]
        if type(dict[key]) == str:
            dict[key] = [dict[key], value]
    return dict


def clean_markdown_links(string_with_markdown):
    """
    Clean strings with markdown links using regex
    "string with [http://link](http://link)" --> "string with http://link"
    https://stackoverflow.com/a/32382747
    """
    return re.sub(r"\[(.*?)\]\((.+?)\)", r"\1", string_with_markdown)


def update_frontend_last_updated_datetime(file_content, new_datetime):
    """
    Update frontend file with regex
    """
    return re.sub("(?<=DATA_LAST_UPDATED_DATETIME: ')(.+?)(?=',)", new_datetime, file_content)
