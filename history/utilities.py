def get_diff_between_two_history_records(new_record, old_record=None, excluded_fields=None, returns="delta"):
    if not old_record:
        if new_record.prev_record:
            old_record = new_record.prev_record
        else:
            raise Exception("get_diff_between_two_history_records old_record not found")

    delta = new_record.diff_against(old_record, excluded_fields=excluded_fields)

    if returns == "changed_fields":
        # flat list of fields
        return delta.changed_fields
    elif returns == "changes":
        # object list : {"field": "test", "old": "previous value", new": "fresh value"}
        return delta.changes
    return delta
