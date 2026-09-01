import pandas as pd


def build_reddit_event_features(reddit_posts):

    reddit_event_features = (
        reddit_posts
        .groupby("event_id")
        .agg(
            average_sentiment=("sentiment_score", "mean"),
            average_investor_relevance=("investor_relevance", "mean"),
            average_importance=("importance", "mean"),
            average_novelty=("novelty", "mean"),
            average_expected_outcome=("expected_outcome", "mean"),
            average_expected_surprise=("expected_surprise", "mean"),
            matched_post_count=("post_id", "count")
        )
        .reset_index()
    )

    return reddit_event_features
