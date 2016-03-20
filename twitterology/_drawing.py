from subprocess import check_call

import pyx
import arrow
from graph_tool.draw import graph_draw
from graph_tool.stats import vertex_average, vertex_hist
from graph_tool.clustering import local_clustering


def user_network_summary(g, output):
    graph_draw(g, output="/tmp/graph.ps", output_size=[300, 300],
               vertex_size=1, vertex_fill_color="blue")
    check_call(["ps2epsi", "/tmp/graph.ps", "/tmp/graph.eps"])

    cv = pyx.canvas.canvas()
    cv.insert(pyx.epsfile.epsfile(0, 0, "/tmp/graph.eps"))

    stats = [
        ["Keyword", g.graph_properties["track"]],
        ["Since", arrow.get(g.edge_properties["created_at"].a.min())],
        ["Till", arrow.get(g.edge_properties["created_at"].a.max())],
        ["Dataset name", g.graph_properties["session"]],
        ["Vertices", g.num_vertices()],
        ["Edges", g.num_edges()],
        ["Avg. degree", float(g.num_edges()) / g.num_vertices()],
        ["Avg. clustering", vertex_average(g, local_clustering(g))[0]]
    ]

    shift = -1
    for key, value in stats:
        cv.text(0, shift, key + ": " + str(value).replace("#", r"\#"))
        shift -= 0.4

    shift -= 5
    degree_distrib = cv.insert(pyx.graph.graphxy(0, shift, width=8, height=5))
    counts, bins = vertex_hist(g, "in")
    degree_distrib.plot(pyx.graph.data.values(x=bins[1:], y=counts))

    cv.writeEPSfile(output)
