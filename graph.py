# coding=gbk

import networkx as nx
import matplotlib.pyplot as plt

import test
import settings

if __name__ == '__main__':
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
