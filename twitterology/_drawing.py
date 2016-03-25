from IPython.display import display, Markdown

import pandas as pd
import arrow

from matplotlib import pyplot as plt

from graph_tool.draw import graph_draw
from graph_tool.stats import vertex_average, vertex_hist
from graph_tool.clustering import local_clustering
from graph_tool.topology import label_largest_component


def user_network_summary(g):
    span = "{:D MMM YYYY, HH:mm} - {:D MMM YYYY, HH:mm}".format(
        arrow.get(g.edge_properties["created_at"].a.min()),
        arrow.get(g.edge_properties["created_at"].a.max())
    )
    largest_component = label_largest_component(g, directed=False).a.sum()

    display(Markdown("### " + g.graph_properties["track"].replace("#", r"\#")))
    display(Markdown("#### " + span))

    graph_draw(g, inline=True, output_size=[1000, 1000],
               vertex_fill_color=[.2, .3, .9, .7], vertex_size=2)
    stats = pd.DataFrame([
        ["Vertices",
         g.num_vertices()],
        ["Edges",
         g.num_edges()],
        ["Avg. degree",
         float(g.num_edges()) / g.num_vertices()],
        ["Avg. clustering",
         vertex_average(g, local_clustering(g))[0]],
        ["Giant component share",
         "{:.1%}".format(largest_component / g.num_vertices())]
    ], columns=["Metric", "Value"])
    display(stats)

    bins = 20
    counts, _ = vertex_hist(g, "in", range(bins))

    plt.bar(range(1, bins), counts, align="center")

    plt.xticks(range(bins))
    plt.xlim([0.5, bins - 1])
    plt.title("Degree distribution")

    plt.show()
