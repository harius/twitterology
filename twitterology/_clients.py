import json

from birdy.twitter import StreamClient, UserClient


def stream_client(config_file="./etc/twitter_api.json"):
    with open(config_file) as opened_config:
        config = json.load(opened_config)

    return StreamClient(**config).stream


def user_client(config_file="./etc/twitter_api.json"):
    with open(config_file) as opened_config:
        config = json.load(opened_config)

    return UserClient(**config).api
