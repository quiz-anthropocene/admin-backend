FILTERS_INGORE_LIST = ["page"]


def form_filters_cleaned_dict(form_cleaned_data):
    return {k: v for (k, v) in form_cleaned_data.items() if ((k not in ["page"]) and v)}


def form_filters_to_list(form_cleaned_data):
    form_filters = list()
    for (key, value) in form_cleaned_data.items():
        if type(value) == list:
            for item in value:
                form_filters.append({"key": key, "value": str(item)})
        else:
            form_filters.append({"key": key, "value": str(value)})
    return form_filters
