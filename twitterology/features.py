from re import findall, UNICODE

import numpy as np
import arrow


class Length(object):
    def __call__(self, tweet):
        length = float(len(tweet["text"]))
        return np.array([length])


class Hashtags(object):
    _hashtag = r"#\w+"

    def __call__(self, tweet):
        hashtags = findall(self._hashtag, tweet["text"], flags=UNICODE)
        count = float(len(hashtags))
        return np.array([count])


class Mentions(object):
    _mention = r"@\w+"

    def __call__(self, tweet):
        mentions = findall(self._mention, tweet["text"], flags=UNICODE)
        count = float(len(mentions))
        return np.array([count])


class Retweet(object):
    def __call__(self, tweet):
        is_retweet = float(bool(tweet["text"].startswith("RT")))
        return np.array([is_retweet])


class Average(object):
    def __init__(self, measure):
        self._measure = measure

    def __call__(self, sequence):
        matrix = np.array([self._measure(item) for item in sequence])
        average = np.average(matrix, axis=0)
        return average


class Median(object):
    def __init__(self, measure):
        self._measure = measure

    def __call__(self, sequence):
        matrix = np.array([self._measure(item) for item in sequence])
        median = np.median(matrix, axis=0)
        return median


class AverageInterval(object):
    _date_format = "ddd MMM DD HH:mm:ss Z YYYY"

    def __call__(self, tweets):
        timestamps = sorted(
            arrow.get(tweet["created_at"], self._date_format)
            for tweet in tweets
        )
        if len(timestamps) < 2:
            average = 0.0
        else:
            deltas = zip(timestamps[:-1], timestamps[1:])
            average = sum(
                (y - x).total_seconds() / 60.0
                for x, y in deltas
            ) / len(deltas)
        return np.array([average])


class Diversity(object):
    _word = r"\w+"

    def __call__(self, tweets):
        words = [
            word for tweet in tweets
            for word in findall(self._word, tweet["text"], flags=UNICODE)
        ]
        diversity = float(len(set(words))) / len(words)
        return np.array([diversity])


class Product(object):
    def __init__(self, *args):
        self._components = args

    def __call__(self, *args):
        features = []
        for component in self._components:
            features.extend(component(*args))
        return features
