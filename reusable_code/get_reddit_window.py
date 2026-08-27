import pandas as pd


def get_reddit_window(event_id, event_date, event_dataset):

    event_date = pd.to_datetime(event_date)

    event_rows = event_dataset[
        event_dataset["event_id"] == event_id
    ]

    day_2_row = event_rows[
        event_rows["day"] == 2
    ]

    day_2_date = pd.to_datetime(
        day_2_row["Date"].iloc[0]
    )

    start_date = event_date
    end_date = day_2_date

    return start_date, end_date