from re import findall, UNICODE

import arrow


class Frequency(object):
    _date_format = "ddd MMM DD HH:mm:ss Z YYYY"

    def __call__(self, tweets):
        timestamps = sorted(
            arrow.get(tweet["created_at"], self._date_format).timestamp
            for tweet in tweets
        )
        if len(timestamps) < 2:
            return [0.0]

        pairs = zip(timestamps[:-1], timestamps[1:])
        return [sum(float(y - x) for x, y in pairs) / len(pairs)]


class Average(object):
    def __call__(self, tweets):
        return [sum(self.operator(tweet) for tweet in tweets) / len(tweets)]


class Length(Average):
    def operator(self, tweet):
        return float(len(tweet["text"]))


class HashtagCount(Average):
    _hashtag = r"#\w+"

    def operator(self, tweet):
        hashtags = findall(self._hashtag, tweet["text"], flags=UNICODE)
        return float(len(hashtags))


class Tuple(object):
    def __init__(self, *args):
        self._features = args

    def __call__(self, tweets):
        result = []
        for feature in self._features:
            result.extend(feature(tweets))
        return result
