# coding=gbk

import networkx as nx
import matplotlib.pyplot as plt
import json

import test
import settings


def store(data):
    with open('miserables2.json', 'w') as json_file:
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


def get_displayed_label(index):
    return ", ".join(map(lambda i: settings.labels[i], settings.clusters[index].cases))


def generate_json():
    size = len(settings.clusters)

    nodes = []
    for i in range(size):
        nodes.append({"id": get_displayed_label(i), "group": 1, "size": len(settings.clusters[i].funcs) + 2})

    links = []
    for i in range(size):
        for j in range(i + 1, size):
            if settings.links[i][j] != 0:
                links.append({"source": get_displayed_label(i), "target": get_displayed_label(j), "value": settings.links[i][j] * 5})

    data = {"nodes": nodes, "links": links}
    store(data)


if __name__ == '__main__':
    test.run_test()
    generate_json()
