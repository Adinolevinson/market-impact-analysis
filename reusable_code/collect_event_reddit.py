import requests
import pandas as pd
import time


def collect_event_reddit(event_id, search_query, start_date, end_date):

    url = "https://arctic-shift.photon-reddit.com/api/posts/search"

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    subreddits = [
        "teslainvestorsclub",
        "stocks",
        "investing",
        "wallstreetbets",
        "teslamotors"
    ]

    all_posts = []

    for subreddit in subreddits:

        current_after = int(start_date.timestamp())

        end_timestamp = int(
            (end_date + pd.Timedelta(days=1)).timestamp()
        )

        while True:

            params = {
                "subreddit": subreddit,
                "after": current_after,
                "before": end_timestamp,
                "sort": "asc",
                "limit": 100
            }

            response = requests.get(
                url,
                params=params,
                timeout=30
            )

            if response.status_code == 429:

                wait_time = int(
                    response.headers.get(
                        "X-RateLimit-Reset",
                        10
                    )
                )

                print(
                    f"Rate limited on {subreddit} "
                    f"for {event_id}. "
                    f"Waiting {wait_time} seconds..."
                )

                time.sleep(wait_time)

                continue

            if response.status_code != 200:

                print(
                    f"Skipped {subreddit} for {event_id}: "
                    f"status {response.status_code}"
                )

                break

            data = response.json()

            batch = data["data"]

            if len(batch) == 0:
                break

            all_posts.extend(batch)

            if len(batch) < 100:
                break

            last_post_time = batch[-1]["created_utc"]

            current_after = last_post_time + 1

            time.sleep(1)

    posts = pd.DataFrame(all_posts)

    if posts.empty:
        return posts

    posts = posts.drop_duplicates(
        subset="id"
    )

    posts["title"] = posts["title"].fillna("")
    posts["selftext"] = posts["selftext"].fillna("")

    posts["search_text"] = (
        posts["title"]
        + " "
        + posts["selftext"]
    ).str.lower()

    search_words = search_query.lower().split()

    posts = posts[
        posts["search_text"].apply(
            lambda text: all(
                word in text
                for word in search_words
            )
        )
    ]

    if posts.empty:
        return posts

    posts["event_id"] = event_id
    posts["search_query"] = search_query

    posts["created_date"] = pd.to_datetime(
        posts["created_utc"],
        unit="s"
    )

    columns = [
        "event_id",
        "id",
        "subreddit",
        "created_date",
        "title",
        "selftext",
        "score",
        "num_comments",
        "url",
        "search_query"
    ]

    posts = posts[columns]

    posts = posts.rename(
        columns={"id": "post_id"}
    )

    return posts