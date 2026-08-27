import pandas as pd

from reusable_code.get_reddit_window import get_reddit_window
from reusable_code.collect_event_reddit import collect_event_reddit
from reusable_code.clean_reddit_posts import clean_reddit_posts


def build_reddit_dataset(events_with_queries, event_dataset):

    all_posts = []

    for _, event in events_with_queries.iterrows():

        event_id = event["event_id"]
        event_date = event["event_date"]
        search_query = event["search_query"]

        start_date, end_date = get_reddit_window(
            event_id,
            event_date,
            event_dataset
        )

        posts = collect_event_reddit(
            event_id,
            search_query,
            start_date,
            end_date
        )

        if posts.empty:
            continue

        posts = clean_reddit_posts(posts)

        all_posts.append(posts)

    reddit_dataset = pd.concat(
        all_posts,
        ignore_index=True
    )

    return reddit_dataset