#!/usr/bin/env python
# Usage: python examples/process.py track '#HelloWorld' 123456 424242
from sys import argv
from re import findall, split, UNICODE

import twitterology as tw

from simhash import Simhash, SimhashIndex
from collections import Counter


import logging
logging.basicConfig(level=logging.ERROR)


SEP = u"tWITteroLOgy"
HASHTAG = r"#\w+"


def extract_tweets(texts):
    return split(SEP, texts, flags=UNICODE)


def extract_hashtags_single(tweet):
    return findall(HASHTAG, tweet, flags=UNICODE)


def extract_hashtags(tweets):
    hashtags = []
    for tweet in tweets:
        hashtags.extend(extract_hashtags_single(tweet))
    return hashtags


def extract_features(tweets):
    hashtags = Counter(extract_hashtags(tweets))
    return hashtags.most_common(5)


def main():
    query = {argv[1]: argv[2], "session": argv[3]}

    source = tw.sources.tweets(**query)
    storage = tw.sources.timelines(source=source.table.name, session=argv[4])

    users = storage.database.query("""
        select
          user__id_str as user_id,
          group_concat(text, '{sep}') as texts
        from [{storage.table.name}]
        group by
          user_id
    """.format(storage=storage, sep=SEP))

    index = SimhashIndex([], k=5)
    sample_hashes = []

    for user in users:
        tweets = extract_tweets(user["texts"])

        full_features = extract_features(tweets[::2])
        sample_features = extract_features(tweets[1::2])
        if not full_features:
            continue

        full_hash = Simhash(full_features)
        sample_hash = Simhash(sample_features)

        index.add(user["user_id"], full_hash)
        sample_hashes.append((user["user_id"], sample_hash))

    total = 0
    successes = 0
    fails = 0
    for user_id, sample_hash in sample_hashes:
        nears = index.get_near_dups(sample_hash)

        total += 1
        if not nears:
            fails += 1
        if len(nears) <= 3 and user_id in nears:
            successes += 1
    
    print successes, "OK,", fails, "FAILS,", total, "TOTAL"


if __name__ == "__main__":
    main()
