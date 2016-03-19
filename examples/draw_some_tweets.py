# -*- coding: utf-8 -*-
import twitterology as tw


if __name__ == "__main__":
    track = "hello"
    session = "20160319-120837"

    storage = tw.sources.tweets(track=track, session=session)
    print len(storage)
    g = tw.user_network(storage)

    tw.user_network_summary(g, "network.eps")
