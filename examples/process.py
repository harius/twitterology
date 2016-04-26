#!/usr/bin/env python
# Usage: python examples/process.py track '#HelloWorld' 123456 424242
from sys import argv
from re import findall, UNICODE

import twitterology as tw

from datasketch import MinHash, MinHashLSH
from simhash import Simhash, SimhashIndex


def extract_hashtags(text):
    return findall(r"#\w+", text, UNICODE)


def main():
    query = {argv[1]: argv[2], "session": argv[3]}

    source = tw.sources.tweets(**query)
    storage = tw.sources.timelines(source=source.table.name, session=argv[4])

    response = storage.database.query("""
        select user__id, group_concat(text) as text
        from [{storage.table.name}]
        group by user__id
    """.format(storage=storage))

    lsh = MinHashLSH(threshold=0.2, num_perm=128)
    foo = {}
    bar = {}
    chosen = None
    for user in response:
        hashtags = extract_hashtags(user["text"])
        if chosen is None and len(set(hashtags)) > 5:
            print "chose", user["user__id"]
            chosen_hashtags = hashtags[::2]
            hashtags = hashtags[1::2]
            chosen = MinHash(num_perm=128)
            for ht in chosen_hashtags:
                chosen.update(ht.encode("utf-8"))

        user_hash = MinHash(num_perm=128)
        for ht in hashtags:
            user_hash.update(ht.encode("utf-8"))

        lsh.insert(user["user__id"], user_hash)
        foo[user["user__id"]] = user_hash
        bar[user["user__id"]] = hashtags

    for x in sorted(lsh.query(chosen), key=lambda x: foo[x].jaccard(chosen)):
        print "candidate", x, foo[x].jaccard(chosen)


if __name__ == "__main__":
    main()
