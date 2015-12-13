#!/usr/bin/env python
import twitterology as tw

import sys
import json


if __name__ == "__main__":
    client = tw.create_stream_client()
    filter_api = client.stream.statuses.filter

    tweets = filter_api.post(track="hello").stream()
    json.dump(next(tweets), sys.stdout, indent=2)
