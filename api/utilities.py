from datetime import datetime, timedelta


def aggregate_timeseries_by_week(timeseries):
    """
    input:
    [{"day": "2020-07-30", "y": 2}, {"day": "2020-08-02", "y": 3}, {"day": "2020-08-03", "y": 4}] # noqa
    output
    [{"day": "2020-07-27", "y": 5}, {"day": "2020-08-03", "y": 4}]
    """
    timeseries_grouped_by_week = []
    # loop on timeseries
    for elem in timeseries:
        # get start-of-week date for each element
        elem_date = datetime.strptime(elem["day"], "%Y-%m-%d")
        elem_week_start_date = elem_date - timedelta(days=elem_date.weekday())
        elem_week_start_date_str = elem_week_start_date.strftime("%Y-%m-%d")
        # get index of start-of-week date
        elem_week_start_date_index = next(
            (
                index
                for (index, d) in enumerate(timeseries_grouped_by_week)
                if d["day"] == elem_week_start_date_str
            ),
            None,
        )
        # add elem to grouped timeseries
        if elem_week_start_date_index is None:
            timeseries_grouped_by_week.append(
                {"day": elem_week_start_date_str, "y": elem["y"]}
            )
        else:
            timeseries_grouped_by_week[elem_week_start_date_index]["y"] += elem["y"]
    # return
    return timeseries_grouped_by_week


# def add_validation_error()
