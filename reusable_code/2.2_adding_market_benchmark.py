import pandas as pd


def add_market_benchmark(
    event_window,
    benchmark_data,
    benchmark_name="SPY"
):
    event_window = event_window.copy()
    benchmark_data = benchmark_data.copy()

    event_window["Date"] = pd.to_datetime(
        event_window["Date"]
    )

    benchmark_data["Date"] = pd.to_datetime(
        benchmark_data["Date"]
    )

    benchmark_close_column = f"{benchmark_name}_Close"
    benchmark_return_column = (
        f"{benchmark_name}_return_from_day_0"
    )

    benchmark_prices = benchmark_data[
        ["Date", "Close"]
    ].rename(
        columns={"Close": benchmark_close_column}
    )

    combined_window = event_window.merge(
        benchmark_prices,
        on="Date",
        how="left"
    )

    benchmark_day_0_close = combined_window.loc[
        combined_window["day"] == 0,
        benchmark_close_column
    ].iloc[0]

    combined_window[benchmark_return_column] = (
        combined_window[benchmark_close_column]
        / benchmark_day_0_close
        - 1
    ) * 100

    combined_window["abnormal_return"] = (
        combined_window["return_from_day_0"]
        - combined_window[benchmark_return_column]
    )

    return combined_window