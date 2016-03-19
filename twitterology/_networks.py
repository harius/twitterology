from collections import defaultdict

from graph_tool import Graph


def user_network(storage):
    g = Graph()
    users = defaultdict(g.add_vertex)

    for tweet in storage:
        tweeter_id = tweet["user__id_str"]
        origin_id = tweet["retweeted_status__user__id_str"]

        if origin_id:
            g.add_edge(users[tweeter_id], users[origin_id])

    return g
