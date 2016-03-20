from sys import argv

import twitterology as tw


if __name__ == "__main__":
    track = argv[1]

    client = tw.stream_client()
    storage = tw.sources.tweets(track=track)

    print "Writing to table", storage.table
    print "%%"

    tweets = client.statuses.filter.post(track=track).stream()
    for tweet in tweets:
        try:
            print tweet["user"]["name"]
            print tweet["text"]
        except KeyError:
            print tweet
            raise
        finally:
            print "%%"

        storage.insert(tw.dump_for_storage(tweet))
