import json
import birdy.twitter


def create_stream_client(config_file="./etc/twitter_api.json"):
    with open(config_file) as opened_config:
        config = json.load(opened_config)

    return birdy.twitter.StreamClient(**config)
