#!/usr/bin/env python
# Usage: examples/guess_half examples.db:track_hello
from sys import argv
from re import findall, split, UNICODE
from itertools import chain, groupby
from operator import itemgetter

import twitterology as tw

from simhash import Simhash, SimhashIndex
from collections import Counter
from tqdm import tqdm


import logging
logging.basicConfig(level=logging.ERROR)

HASHTAG = r"#\w+"
MENTION = r"@\w+"
RETWEET = r"^RT @[^:]+:"


def extract_hashtags_single(tweet):
    if extract_retweets_single(tweet):
        return []
    return findall(HASHTAG, tweet["text"], flags=UNICODE)


def extract_mentions_single(tweet):
    if extract_retweets_single(tweet):
        return []
    return findall(MENTION, tweet["text"], flags=UNICODE)


def extract_retweets_single(tweet):
    return findall(RETWEET, tweet["text"], flags=UNICODE)


def extract_hashtags(tweets):
    return chain.from_iterable(map(extract_hashtags_single, tweets))


def extract_mentions(tweets):
    return chain.from_iterable(map(extract_mentions_single, tweets))


def extract_retweets(tweets):
    return chain.from_iterable(map(extract_retweets_single, tweets))


def extract_features(tweets, h, m, r):
    hashtags = Counter(extract_hashtags(tweets))
    mentions = Counter(extract_mentions(tweets))
    retweets = Counter(extract_retweets(tweets))
    return ([]
        + [(h, x * 0.60) for h, x in hashtags.most_common(h)]
        + [(m, x * 1.00) for m, x in mentions.most_common(m)]
        + [(r, x * 0.02) for r, x in retweets.most_common(r)]
    )


def main(f, k, h, m, r):
    database, table = argv[1].split(":")
    print "=== building ==="
    print f, k, h, m, r

    storage = tw.sources.sqlite(database, table)
    tweets = storage.find(order_by="user__id_str")

    user_count = sum(1 for _ in storage.distinct("user__id_str"))

    index = SimhashIndex([], f=f, k=k)

    full_hashes = {}
    sample_hashes = {}

    for user_id, user_tweets in tqdm(groupby(tweets, itemgetter("user__id_str")), total=user_count):
        user_tweets = list(user_tweets)

        full_features = extract_features(user_tweets[::2], h=h, m=m, r=r)
        sample_features = extract_features(user_tweets[1::2], h=h, m=m, r=r)

        full_hash = Simhash(full_features, f=f)
        sample_hash = Simhash(sample_features, f=f)

        index.add(user_id, full_hash)

        full_hashes[user_id] = full_hash
        sample_hashes[user_id] = sample_hash

    print "=== validating ==="

    total = 0
    sum_nears = 0.0
    successes = 0
    fails = 0

    for user_id, sample_hash in sample_hashes.iteritems():
        near_ids = index.get_near_dups(sample_hash)

        total += 1
        sum_nears += len(near_ids)
        if not near_ids:
            fails += 1
            continue

        nearest = min(
            near_ids,
            key=lambda near_id: sample_hash.distance(full_hashes[near_id])
        )
        if nearest == user_id:
            successes += 1

    print successes, "OK,", fails, "FAILS,", total, "TOTAL,", sum_nears / total, "AVG. GUESSES"


if __name__ == "__main__":
    main(f=64, k=0, h=1, m=1, r=1)
