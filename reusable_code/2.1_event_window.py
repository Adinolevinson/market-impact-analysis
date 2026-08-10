import pandas as pd


def get_event_window(event_id, events_data, stock_data):

    events_data = events_data.copy()
    stock_data = stock_data.copy()

    events_data["event_date"] = pd.to_datetime(
    events_data["event_date"]
)

    stock_data["Date"] = pd.to_datetime(
        stock_data["Date"]
    )


    # Find the event with the matching event_id
    event = events_data[
        events_data["event_id"] == event_id
    ].iloc[0]

    # Get the event date
    event_date = event["event_date"]

    # Find the first trading day on or after the event date
    possible_days = stock_data[
        stock_data["Date"] >= event_date
    ]

    # Get the row number of that trading day
    event_index = possible_days.index[0]

    # Create a window from Day 0 to Day 5
    stocks_window = stock_data.iloc[
        event_index - 1 : event_index + 5
    ].copy()

    # Label the rows Day 0 to Day 5
    stocks_window["day"] = range(0, len(stocks_window))

    # Get the closing price on Day 0
    baseline_price = stocks_window.iloc[0]["Close"]

    # Calculate percentage movement from Day 0
    stocks_window["return_from_day_0"] = (
        stocks_window["Close"] / baseline_price - 1
    ) * 100

    # Add event information
    stocks_window["event_id"] = event["event_id"]
    stocks_window["event_name"] = event["event_name"]
    stocks_window["event_type"] = event["event_type"]
    stocks_window["event_date"] = event_date

    # Return the useful columns
    return stocks_window[
        [
            "event_id",
            "event_name",
            "event_type",
            "event_date",
            "day",
            "Date",
            "Close",
            "return_from_day_0"
        ]
    ]
