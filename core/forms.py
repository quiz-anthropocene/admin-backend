from urllib.parse import urlencode


FILTERS_INGORE_LIST = ["page"]


def form_filters_cleaned_dict(form_cleaned_data):
    return {k: v for (k, v) in form_cleaned_data.items() if ((k not in ["page"]) and v)}


def form_filters_to_list(form_cleaned_data, with_delete_url=False):
    form_filters_list = list()
    form_filters_urlencode = f"?{urlencode(form_cleaned_data)}"
    for (key, value) in form_cleaned_data.items():
        if type(value) == list:
            for item in value:
                form_filters_list.append({"key": key, "value": str(item), "value_id": value.id})
        else:
            form_filters_list.append({"key": key, "value": str(value)})
    if with_delete_url:
        for index, filter in enumerate(form_filters_list):
            filter_key = filter["key"]
            filter_value = filter.get("value_id", filter["value"])
            form_filters_list[index]["delete_url"] = form_filters_urlencode.replace(f"{filter_key}={filter_value}", "")
    return form_filters_list
