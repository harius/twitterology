from re import findall, UNICODE
from collections import Counter

import numpy as np
import arrow


class Length(object):
    def __call__(self, tweet):
        return float(len(tweet["text"]))


class IsRetweet(object):
    def __call__(self, tweet):
        return float(tweet["text"].startswith("RT"))


class IncludesLink(object):
    def __call__(self, tweet):
        return float("https://t.co" in tweet["text"])


class Hashtags(object):
    _hashtag = r"#\w+"

    def __call__(self, tweet):
        return findall(self._hashtag, tweet["text"], flags=UNICODE)


class Mentions(object):
    _mention = r"@\w+"

    def __call__(self, tweet):
        return findall(self._mention, tweet["text"], flags=UNICODE)


class Count(object):
    def __init__(self, what):
        self._what = what

    def __call__(self, tweet):
        return float(len(self._what(tweet)))


class Counts(object):
    length = 1

    def __init__(self, what, top=None):
        self._what = what
        self._top = top

    def __call__(self, tweets):
        counter = Counter()
        for tweet in tweets:
            counter.update(self._what(tweet))

        frequent = dict(counter.most_common(self._top))
        return np.array([Counter(frequent)])


class Average(object):
    length = 1

    def __init__(self, measure):
        self._measure = measure

    def __call__(self, tweets):
        if tweets:
            average = np.average([self._measure(tweet) for tweet in tweets])
        else:
            average = 0.0
        return np.array([average])


class Median(object):
    length = 1

    def __init__(self, measure):
        self._measure = measure

    def __call__(self, tweets):
        if tweets:
            median = np.median([self._measure(tweet) for tweet in tweets])
        else:
            median = 0.0
        return np.array([median])


class AverageInterval(object):
    date_format = "ddd MMM DD HH:mm:ss Z YYYY"
    length = 1

    def __call__(self, tweets):
        timestamps = sorted(
            arrow.get(tweet["created_at"], self.date_format)
            for tweet in tweets
        )
        if len(timestamps) >= 2:
            deltas = zip(timestamps[:-1], timestamps[1:])
            average = sum(
                (y - x).total_seconds() / 60.0
                for x, y in deltas
            ) / len(deltas)
        else:
            average = 0.0
        return np.array([average])


class Diversity(object):
    word = r"\w+"
    length = 1

    def __call__(self, tweets):
        words = [
            word for tweet in tweets
            for word in findall(self.word, tweet["text"], flags=UNICODE)
        ]
        if words:
            diversity = float(len(set(words))) / len(words)
        else:
            diversity = 0.0
        return np.array([diversity])


class Product(object):
    def __init__(self, *args):
        self._components = args
        self.length = sum(
            component.length for component in self._components
        )

    def __call__(self, *args):
        features = []
        for component in self._components:
            features.extend(component(*args))
        return np.array(features)


class AbsoluteDifference(object):
    def __init__(self, features):
        self.features = features

    def __call__(self, one, other):
        return np.absolute(one - other)


class JaccardDifference(object):
    count = np.vectorize(lambda c: sum(c.values()), otypes='f')

    def __init__(self, features):
        self.features = features

    def __call__(self, one, other):
        return 1.0 - self.count(one & other) / (1 + self.count(one | other))


class ProductDifference(object):
    def __init__(self, *args):
        self._components = args
        self.features = Product(
            *[component.features for component in self._components]
        )

    def __call__(self, one, other):
        features = []

        offset = 0
        for component in self._components:
            length = component.features.length
            features.extend(component(
                one[offset:offset + length],
                other[offset:offset + length]
            ))
            offset += length

        return np.array(features)
