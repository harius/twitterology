import twitterology as tw


if __name__ == "__main__":
    client = tw.create_stream_client()
    tweets = tw.sources.raw_tweets("example_table")

    with tw.logged_api_call(client,
                            "stream.statuses.filter",
                            track="hello") as filtered_tweets:
        for tweet in filtered_tweets.stream():
            print tweet["user"]["name"]
            print tweet["text"]
            print "%%"

            tweets.insert(tw.prepare_for_db(tweet))
