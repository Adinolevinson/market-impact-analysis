import pandas as pd


def build_event_features(event_data):

    selected_days = event_data[
        event_data["day"].isin([1, 3, 5])
    ][
        ["event_id", "event_name", "event_type", "day", "abnormal_return"]
    ].copy()

    selected_days["absolute_abnormal_return"] = (
        selected_days["abnormal_return"].abs()
    )

    event_features = selected_days.pivot(
        index=["event_id", "event_name", "event_type"],
        columns="day",
        values=["abnormal_return", "absolute_abnormal_return"]
    )

    event_features.columns = [
        f"day_{day}_{return_type}"
        for return_type, day in event_features.columns
    ]

    event_features = event_features.reset_index()

    return event_features
