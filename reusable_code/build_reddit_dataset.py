import os
import pandas as pd

from reusable_code.get_reddit_window import get_reddit_window
from reusable_code.collect_event_reddit import collect_event_reddit
from reusable_code.clean_reddit_posts import clean_reddit_posts


def build_reddit_dataset(events_with_queries, event_dataset):

    all_posts = []

    output_folder = "../data/processed/reddit/events"

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    for _, event in events_with_queries.iterrows():

        event_id = event["event_id"]
        event_date = event["event_date"]
        search_query = event["search_query"]

        print(f"Collecting Reddit posts for {event_id}")

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
            print(f"No posts found for {event_id}")
            continue

        posts = clean_reddit_posts(posts)

        posts.to_csv(
            f"{output_folder}/{event_id}_reddit.csv",
            index=False
        )

        print(
            f"Saved {len(posts)} posts for {event_id}"
        )

        all_posts.append(posts)

    if not all_posts:
        return pd.DataFrame()

    reddit_dataset = pd.concat(
        all_posts,
        ignore_index=True
    )

    return reddit_dataset