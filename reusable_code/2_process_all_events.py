import pandas as pd

from reusable_code.event_window import get_event_window
from reusable_code.adding_market_benchmark import add_market_benchmark

def process_all_events(events, company_data, benchmark_data):
    all_event_windows = []

    for event_id in events["event_id"]:
        event_window = get_event_window(
            event_id,
            events,
            company_data
        )

        event_window_with_benchmark = add_market_benchmark(
            event_window,
            benchmark_data,
            benchmark_name="SPY"
        )

        all_event_windows.append(event_window_with_benchmark)

    return pd.concat(all_event_windows, ignore_index=True)