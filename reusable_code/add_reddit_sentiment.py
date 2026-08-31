import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def add_reddit_sentiment(posts):

    posts = posts.copy()

    analyzer = SentimentIntensityAnalyzer()

    posts["sentiment_score"] = posts["text"].apply(
        lambda text: analyzer.polarity_scores(text)["compound"]
    )

    return posts