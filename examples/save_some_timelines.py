# Usage: python examples/save_some_timelines track '#HelloWorld'
from sys import argv

import twitterology as tw


if __name__ == "__main__":
    query = {argv[1]: argv[2], "session": argv[3]}

    client = tw.user_client()

    source = tw.sources.tweets(**query)
    storage = tw.sources.timelines(source=source.table.name)

    for row in source:
        print row["user__id"]

        timeline = client.statuses.user_timeline.get(
            user_id=row["user__id"],
            count=50
        )
        for tweet in timeline.data:
            storage.upsert(tw.dump_for_storage(tweet), ["id_str"])
