#!/usr/bin/env python
# Usage: examples/save_timelines examples.db:track_hello examples.db:timelines_hello
from sys import argv, stdout
from multiprocessing import Pool
from time import sleep
from datetime import datetime
from random import Random
from itertools import imap

import twitterology as tw
from tqdm import tqdm


def gather_user_timeline(user_id, count=100):
    client = tw.user_client()
    try:
        timeline = client.statuses.user_timeline.get(
            user_id=user_id,
            count=count
        )
        return True, [tw.dump_for_storage(tweet) for tweet in timeline.data]
    except tw.ClientException as ex:
        if 'Invalid API resource.' not in str(ex) and 'unknown error' not in str(ex):
            print "sleeping:", str(ex)
            stdout.flush()
            sleep(60 * 7)
    return False, str(ex)


def main():
    from_file, to_location = argv[1:]
    to_database, to_table = to_location.split(":")

    user_ids = []
    with open(from_file) as from_stream:
        for line in from_stream:
            user_id, tweets = line.split("\t")
            user_id = int(user_id)
            tweets = int(tweets)
            if 50 <= tweets <= 9000:
                user_ids.append(user_id)

    rnd = Random(42)
    rnd.shuffle(user_ids)

    storage = tw.sources.sqlite(
        to_database, to_table
    )
    # pool = Pool(4)

    stopped_at = max(
        user_ids.index(row["user__id"])
        for row in storage.distinct("user__id")
        if row["user__id"] in user_ids
    )
    user_ids = user_ids[stopped_at + 1:]

    results = imap(gather_user_timeline, user_ids)
    for index, (is_success, data) in enumerate(results, start=1):
        print "[", index, "/", len(user_ids), "]"

        if is_success:
            if data:
                print "dumping:", data[0]["user__id"]

            for tweet in data:
                print "{}".format(datetime.now())
                storage.insert(tweet)
            print "dumped"
        else:
            print "fail:", data


if __name__ == "__main__":
    main()
