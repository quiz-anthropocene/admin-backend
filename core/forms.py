FILTERS_INGORE_LIST = ["page"]


def form_filters_cleaned_dict(form_cleaned_data):
    return {k: v for (k, v) in form_cleaned_data.items() if ((k not in ["page"]) and v)}


def form_filters_to_list(form_cleaned_data, with_delete_url=False):
    """
    Example:
    - form_cleaned_data: {'category': <Category: Climat>, 'visibility': 'PUBLIC'}
    - form_filters_urlencode: ?category=1&visibility=PUBLIC
    """
    form_filters_list = list()

    for (key, value) in form_cleaned_data.items():
        if type(value) == list:
            for item in value:
                form_filters_list.append({"key": key, "value": str(item), "value_id": getattr(item, "id", None)})
        else:
            form_filters_list.append({"key": key, "value": str(value), "value_id": getattr(value, "id", None)})

    if with_delete_url:
        # first loop to replace the FK/M2M values with their value_ids
        # form_filters_urlencode = f"?{urlencode(form_cleaned_data)}" doesn't work
        form_filters_urlencode = "?" + "&".join(
            [f"{filter['key']}={filter['value_id'] or filter['value']}" for filter in form_filters_list]
        )
        # second loop to build the delete_url
        for index, filter in enumerate(form_filters_list):
            filter_key = filter["key"]
            filter_value = filter["value_id"] or filter["value"]
            form_filters_list[index]["delete_url"] = (
                form_filters_urlencode.replace(f"{filter_key}={filter_value}", "")
                .replace("?&", "?")
                .replace("&&", "&")
            )

    return form_filters_list
