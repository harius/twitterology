from collections import defaultdict

import arrow
from graph_tool import Graph


DATE_FORMAT = "ddd MMM DD HH:mm:ss Z YYYY"


def user_network(storage, track, session):
    g = Graph()
    users = defaultdict(g.add_vertex)

    g.graph_properties["track"] = g.new_graph_property("string", track)
    g.graph_properties["session"] = g.new_graph_property("string", session)

    g.edge_properties["created_at"] = g.new_edge_property("int64_t")

    for tweet in storage:
        tweeter_id = tweet["user__id_str"]
        origin_id = tweet["retweeted_status__user__id_str"]

        created_at = arrow.get(tweet["created_at"], DATE_FORMAT).timestamp

        if origin_id:
            edge = g.add_edge(users[tweeter_id], users[origin_id])
            g.edge_properties["created_at"][edge] = created_at

    return g
