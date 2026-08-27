import pandas as pd


def build_event_search_queries(events):

    events = events.copy()

    def create_query(row):

        event_name = row["event_name"].lower()
        event_type = row["event_type"].lower()

        if "earnings" in event_type:
            return "Tesla earnings"

        elif "recall" in event_type:
            return "Tesla recall"

        elif "pricing" in event_type:
            return "Tesla price"

        elif "product" in event_type:

            if "cybertruck" in event_name:
                return "Tesla Cybertruck"

            elif "plaid" in event_name:
                return "Tesla Model S Plaid"

            elif "semi" in event_name:
                return "Tesla Semi"

        elif "factory" in event_type:
            return "Tesla factory"

        elif "technology" in event_type:

            event_name = row["event_name"].lower()

            if "ai day" in event_name:
                return "Tesla AI Day"

            elif "robotaxi" in event_name:
                return "Tesla Robotaxi"

            else:
                return f'Tesla {row["event_name"]}'

        elif "corporate" in event_type:
            return f'Tesla {row["event_name"]}'

        else:
            return f'Tesla {row["event_name"]}'

    events["search_query"] = events.apply(create_query, axis=1)

    return events