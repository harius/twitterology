# -*- coding: utf-8 -*-
from sys import argv

import twitterology as tw


if __name__ == "__main__":
    track, session = argv[1:3]

    storage = tw.sources.tweets(track=track, session=session)
    g = tw.user_network(storage, track=track, session=session)

    tw.user_network_summary(g, track)
