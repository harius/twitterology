#!/usr/bin/env python
import twitterology as tw


if __name__ == "__main__":
    client = tw.create_stream_client()
    with tw.logged_api_call(
            client, "stream.statuses.filter", track="hello"
    ) as filtered_tweets:
        for tweet in filtered_tweets.stream():
            print "---"
            print tweet["text"]
