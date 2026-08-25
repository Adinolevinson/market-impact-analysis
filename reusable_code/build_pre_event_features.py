import pandas as pd


def get_pre_event_abnormal_return(event_date, stock_data, benchmark_data):

    event_date = pd.to_datetime(event_date)

    stock_data["Date"] = pd.to_datetime(stock_data["Date"])
    benchmark_data["Date"] = pd.to_datetime(benchmark_data["Date"])

    stock_before_event = stock_data[
        stock_data["Date"] < event_date
    ].sort_values("Date")

    benchmark_before_event = benchmark_data[
        benchmark_data["Date"] < event_date
    ].sort_values("Date")

    stock_recent_days = stock_before_event.tail(6)
    benchmark_recent_days = benchmark_before_event.tail(6)

    stock_day_minus_5_close = stock_recent_days.iloc[0]["Close"]
    stock_day_0_close = stock_recent_days.iloc[-1]["Close"]

    benchmark_day_minus_5_close = benchmark_recent_days.iloc[0]["Close"]
    benchmark_day_0_close = benchmark_recent_days.iloc[-1]["Close"]

    stock_return = (
        (stock_day_0_close / stock_day_minus_5_close) - 1
    ) * 100

    benchmark_return = (
        (benchmark_day_0_close / benchmark_day_minus_5_close) - 1
    ) * 100

    pre_event_5_day_abnormal_return = (
        stock_return - benchmark_return
    )

    return pre_event_5_day_abnormal_return


def build_pre_event_features(
    event_features,
    event_dataset,
    stock_data,
    benchmark_data
):

    event_dates = event_dataset[
        ["event_id", "event_date"]
    ].drop_duplicates()

    features = event_features.merge(
        event_dates,
        on="event_id"
    )

    features["pre_event_5_day_abnormal_return"] = (
        features["event_date"].apply(
            lambda date: get_pre_event_abnormal_return(
                date,
                stock_data,
                benchmark_data
            )
        )
    )

    if "pre_event_5_day_return" in features.columns:
        features = features.drop(
            columns="pre_event_5_day_return"
        )

    features.to_csv(
        "../data/processed/tesla_event_features.csv",
        index=False
    )

    return features