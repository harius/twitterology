#!/usr/bin/env python
# -*- coding: utf-8 -*-
import twitterology as tw


if __name__ == "__main__":
    print "=== tweets ==="
    for params in tw.sources.tweets():
        print " ".join("'" + param + "'" for param in params)

    print "=== timelines ==="
    for params in tw.sources.timelines():
        print " ".join("'" + param + "'" for param in params)
