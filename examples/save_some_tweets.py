import twitterology as tw
import twitterology.sources as tws


if __name__ == "__main__":
    client = tw.create_stream_client()
    raw_tweets = tws.raw_tweets("example_table")

    with tw.logged_api_call(client,
                            "stream.statuses.filter",
                            track="hello") as filtered_tweets:
        for tweet in filtered_tweets.stream():
            print tweet["text"]
            print "---"

            raw_tweets.insert(tw.prepare_for_db(tweet))
