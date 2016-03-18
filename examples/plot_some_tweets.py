# -*- coding: utf-8 -*-
import twitterology as tw


if __name__ == "__main__":
    tweets = tw.sources.raw_tweets("example_table")
    g, _ = tw.build_user_network(tweets)
    tw.network_draw(g, "network.eps")
