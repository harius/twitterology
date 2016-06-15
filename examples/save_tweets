#!/usr/bin/env python
# Usage: examples/save_tweets track     '#Hello'              examples.db:track_hello
#    Or: examples/save_tweets locations '54.2,35.1,57.0,40.2' examples.db:locations_moscow
from sys import argv

from requests.exceptions import ChunkedEncodingError

import twitterology as tw


if __name__ == "__main__":
    method, argument, location = argv[1:]
    database, table = location.split(":")

    client = tw.stream_client()
    storage = tw.sources.sqlite(
        database, table,
        metadata={"method": method, "argument": argument}
    )

    while True:
        try:
            tweets = client.statuses.filter.post(**{method: argument}).stream()
            for tweet in tweets:
                print tweet["user"]["name"]
                print tweet["text"]
                print "%%"
                storage.upsert(tw.dump_for_storage(tweet), ["id_str"])
        except (KeyError, ChunkedEncodingError):
            pass
