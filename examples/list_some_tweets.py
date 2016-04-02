#!/usr/bin/env python
# -*- coding: utf-8 -*-
import twitterology as tw


if __name__ == "__main__":
    for params in tw.sources.tweets():
        print " ".join("'" + param + "'" for param in params)
