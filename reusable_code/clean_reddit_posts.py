def clean_reddit_posts(posts):

    posts = posts.copy()

    posts["selftext"] = posts["selftext"].replace(
        ["[deleted]", "[removed]"],
        ""
    )

    posts["text"] = (
        posts["title"].fillna("")
        + " "
        + posts["selftext"].fillna("")
    ).str.strip()

    return posts
