from subprocess import check_call

import pyx
from graph_tool.draw import graph_draw
from graph_tool.stats import vertex_average, vertex_hist
from graph_tool.clustering import local_clustering


def user_network_summary(g, output):
    graph_draw(g, output="/tmp/graph.ps", output_size=[300, 300],
               vertex_size=2)
    check_call(["ps2epsi", "/tmp/graph.ps", "/tmp/graph.eps"])

    cv = pyx.canvas.canvas()
    cv.insert(pyx.epsfile.epsfile(0, 0, "/tmp/graph.eps"))

    stats = [
        ["Vertices", g.num_vertices()],
        ["Edges", g.num_edges()],
        ["Avg. degree", float(g.num_edges()) / g.num_vertices()],
        ["Avg. clustering", vertex_average(g, local_clustering(g))[0]]
    ]
    for row, (key, value) in enumerate(stats):
        cv.text(0, -1 - row * 0.4, key + ": " + str(value))

    degree_distrib = cv.insert(pyx.graph.graphxy(0, -8, width=8))
    counts, bins = vertex_hist(g, "in")
    degree_distrib.plot(pyx.graph.data.values(x=bins[1:], y=counts))

    cv.writeEPSfile(output)
