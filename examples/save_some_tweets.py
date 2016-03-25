# Usage: python examples/save_some_tweets.py track     '#HelloWorld'
#    Or: python examples/save_some_tweets.py locations '54.2,35.1,57.0,40.2'
from sys import argv

from requests.exceptions import ChunkedEncodingError

import twitterology as tw


if __name__ == "__main__":
    query = {argv[1]: argv[2]}

    client = tw.stream_client()
    storage = tw.sources.tweets(**query)

    print "Writing to table", storage.table
    print "%%"

    while True:
        try:
	    tweets = client.statuses.filter.post(**query).stream()
	    for tweet in tweets:
	        print tweet["user"]["name"]
		print tweet["text"]
	        print "%%"
		storage.upsert(tw.dump_for_storage(tweet), ["id_str"])
	except (KeyError, ChunkedEncodingError):
	    pass
