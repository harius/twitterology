# Usage: python examples/save_some_tweets.py track     '#HelloWorld'
#    Or: python examples/save_some_tweets.py locations '54.2,35.1,57.0,40.2'
from sys import argv

import twitterology as tw


if __name__ == "__main__":
    query = {argv[1]: argv[2]}

    client = tw.stream_client()
    storage = tw.sources.tweets(**query)

    print "Writing to table", storage.table
    print "%%"

    tweets = client.statuses.filter.post(**query).stream()
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
