#!/usr/bin/env python
# Usage: examples/save_timelines examples.db:track_hello examples.db:timelines_hello
from sys import argv
from multiprocessing import Pool
from time import sleep
from datetime import datetime

import twitterology as tw


def gather_user_timeline(user_id, count=50):
    client = tw.user_client()
    try:
        timeline = client.statuses.user_timeline.get(
            user_id=user_id,
            count=count
        )
        return True, [tw.dump_for_storage(tweet) for tweet in timeline.data]
    except tw.ClientException as ex:
        sleep(60 * 20)
        return False, str(ex)


def main():
    from_location, to_location = argv[1:]
    from_database, from_table = from_location.split(":")
    to_database, to_table = to_location.split(":")

    source = tw.sources.sqlite(from_database, from_table)
    user_ids = [row["user__id"] for row in source.distinct("user__id")]

    storage = tw.sources.sqlite(
        to_database, to_table,
        metadata={"origin": from_location}
    )
    pool = Pool(4)

    results = pool.imap_unordered(gather_user_timeline, user_ids)
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
