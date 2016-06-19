# coding: utf-8
from re import findall, UNICODE
from collections import Counter

import numpy as np
import arrow


class Length(object):
    label = "длина текста"

    def __call__(self, tweet):
        return float(len(tweet["text"]))


class IsRetweet(object):
    label = "частота ретвитов"

    def __call__(self, tweet):
        return float(tweet["text"].startswith("RT"))


class IncludesLink(object):
    label = "частота ссылок"

    def __call__(self, tweet):
        return float("https://t.co" in tweet["text"])


class Time(object):
    date_format = "ddd MMM DD HH:mm:ss Z YYYY"
    label = "время публикации"

    def __call__(self, tweet):
        time = arrow.get(tweet["created_at"], self.date_format)
        return time.hour * 60.0 + time.minute


class Hashtags(object):
    label = "хэштегов"
    _hashtag = r"#\w+"

    def __call__(self, tweet):
        return findall(self._hashtag, tweet["text"], flags=UNICODE)


class Mentions(object):
    label = "упоминаний"
    _mention = r"@\w+"

    def __call__(self, tweet):
        return findall(self._mention, tweet["text"], flags=UNICODE)


class Words(object):
    label = "слов"
    _word = r"\w+"

    def __call__(self, tweet):
        return findall(self._word, tweet["text"], flags=UNICODE)


class Count(object):
    def __init__(self, what):
        self._what = what
        self.label = "число " + self._what.label

    def __call__(self, tweet):
        return float(len(self._what(tweet)))


class Counts(object):
    length = 1

    def __init__(self, what, top=None):
        self._what = what
        self._top = top
        self.labels = ["Множ-во популярных " + self._what.label]

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
        self.labels = ["Средн. " + self._measure.label]

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
        self.labels = ["Медиан. " + self._measure.label]

    def __call__(self, tweets):
        if tweets:
            median = np.median([self._measure(tweet) for tweet in tweets])
        else:
            median = 0.0
        return np.array([median])


class AverageInterval(object):
    length = 1

    date_format = "ddd MMM DD HH:mm:ss Z YYYY"
    labels = ["Средн. интервал"]

    def __call__(self, tweets):
        timestamps = sorted(
            arrow.get(tweet["created_at"], self.date_format)
            for tweet in tweets
        )
        if len(timestamps) >= 2:
            deltas = zip(timestamps[:-1], timestamps[1:])
            average = sum(
                min((y - x).total_seconds() / 60.0 / 60.0, 24.0 * 14.0)
                for x, y in deltas
            ) / len(deltas)
        else:
            average = 0.0
        return np.array([average])


class Diversity(object):
    length = 1

    word = r"\w+"
    labels = ["Повторяемость"]

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
        self.components = args
        self.length = sum(component.length for component in args)
        self.labels = [label for component in self.components for label in component.labels]

    def __call__(self, *args):
        features = []
        for component in self.components:
            features.extend(component(*args))
        return np.array(features)


class AbsoluteDifference(object):
    def __init__(self, features):
        self.features = features

    def __call__(self, one, other):
        return np.absolute(one - other)


class JaccardDifference(object):
    count = np.vectorize(len)

    def __init__(self, features):
        self.features = features

    def __call__(self, one, other):
        count_intersections = self.count(one & other)

        count_unions = self.count(one | other)
        count_unions[count_unions == 0] = 1

        return 1.0 - count_intersections.astype("float64") / count_unions


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
