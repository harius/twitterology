# coding: utf-8
from IPython.display import display, Markdown

import pandas as pd
import arrow

from matplotlib import pyplot as plt

from graph_tool.draw import graph_draw
from graph_tool.stats import vertex_average, vertex_hist
from graph_tool.clustering import local_clustering


def user_network_summary(g):
    span = u"{:D MMM YYYY, HH:mm} \u2014 {:D MMM YYYY, HH:mm}".format(
        arrow.get(g.edge_properties["created_at"].a.min()),
        arrow.get(g.edge_properties["created_at"].a.max())
    )

    display(Markdown("### " + g.graph_properties["track"].replace("#", r"\#")))
    display(Markdown("#### " + span))

    graph_draw(g, inline=True, output_size=[1000, 1000],
               vertex_fill_color=[.2, .3, .9, .7], vertex_size=2)

    stats = pd.DataFrame([
        [u"Вершин", g.num_vertices()],
        [u"Рёбер", g.num_edges()],
        [u"Средняя степень", float(g.num_edges()) / g.num_vertices()],
        [u"Средий к. кластеризации", vertex_average(g, local_clustering(g))[0]]
    ], columns=[u"Метрика", u"Значение"])
    display(stats)

    bins = 20
    counts, _ = vertex_hist(g, "in", range(bins))

    plt.bar(range(1, bins), counts, align="center")

    plt.xticks(range(bins))
    plt.xlim([0.5, bins - 1])
    plt.title(u"Распределение степени")
    plt.show()
