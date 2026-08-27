import requests
import pandas as pd


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

        params = {
            "subreddit": subreddit,
            "title": search_query,
            "after": start_date.strftime("%Y-%m-%d"),
            "before": (end_date + pd.Timedelta(days=1)).strftime("%Y-%m-%d"),
            "sort": "asc",
            "limit": 100
        }

        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        if response.status_code != 200:
            print(
                f"Skipped {subreddit} for {event_id}: "
                f"status {response.status_code}"
            )
            continue

        data = response.json()

        all_posts.extend(data["data"])

    posts = pd.DataFrame(all_posts)

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