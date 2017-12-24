# coding=gbk

import networkx as nx
import matplotlib.pyplot as plt
import json

import algorithm
import test
import settings


def store2json(filename, data):
    with open(filename, 'w') as json_file:
        json_file.write(json.dumps(data, indent=2))


def old_way():
    test.run_test()

    G = nx.Graph()

    keys = settings.test_set.keys()
    for i in range(0, len(keys)):
        for j in range(i + 1, len(keys)):
            G.add_edge(keys[i], keys[j], weight=settings.links[i][j])

    # G.add_edge('A', 'B', weight=0.1)
    # G.add_edge('B', 'D', weight=2)
    # G.add_edge('A', 'C', weight=3)
    # G.add_edge('C', 'D', weight=4)

    nx.draw(G, with_labels=True)
    plt.show()


def generate_force_layout():
    size = len(settings.clusters)

    nodes = []
    for i in range(size):
        nodes.append({"id": settings.clusters[i].get_name(), "group": 1, "size": len(settings.clusters[i].funcs) + 2})

    links = []
    for i in range(size):
        for j in range(i + 1, size):
            if settings.links[i][j] != 0:
                links.append({"source": settings.clusters[i].get_name(), "target": settings.clusters[j].get_name(), "value": settings.links[i][j] * 5})

    data = {"nodes": nodes, "links": links}
    store2json('miserables2.json', data)


if __name__ == '__main__':
    test.run_test()
    # algorithm.do_clustering()
    test.print_links()
    test.print_clusters()
    generate_force_layout()
