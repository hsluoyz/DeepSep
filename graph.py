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
            G.add_edge(keys[i], keys[j], weight=settings.test_graph[i][j])

    # G.add_edge('A', 'B', weight=0.1)
    # G.add_edge('B', 'D', weight=2)
    # G.add_edge('A', 'C', weight=3)
    # G.add_edge('C', 'D', weight=4)

    nx.draw(G, with_labels=True)
    plt.show()


if __name__ == '__main__':
    test.run_test()

    nodes = []
    for key in settings.test_set:
        nodes.append({"id": key, "group": 1, "size": len(settings.test_set[key]) + 2})

    links = []
    keys = settings.test_set.keys()
    for i in range(0, len(keys)):
        for j in range(i + 1, len(keys)):
            if settings.test_graph[i][j] != 0:
                links.append({"source": keys[i], "target": keys[j], "value": settings.test_graph[i][j] * 5})

    data = {}
    data["nodes"] = nodes
    data["links"] = links
    store(data)
