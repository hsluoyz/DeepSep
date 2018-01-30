# coding=gbk

import test
import settings
import graph

import random
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans


# 获得相似度矩阵
def get_w():
    size = len(settings.links)
    w = np.zeros((size, size))
    for i in range(size):
        for j in range(i + 1, size):
            val = round(settings.links[i][j], 3)
            if val < 0.1:
                val = 0
            w[i][j] = w[j][i] = val
    return w


# 获得度矩阵
def get_d(w):
    points_num = len(w)
    d = np.diag(np.zeros(points_num))
    for i in range(points_num):
        d[i][i] = sum(w[i])
    return d


# 从拉普拉斯矩阵获得特征矩阵
def get_eig_vec(L, cluster_num):
    eigval, eigvec = np.linalg.eig(L)
    dim = len(eigval)
    dictEigval = dict(zip(eigval, range(0, dim)))
    kEig = np.sort(eigval)[0:cluster_num]
    ix = [dictEigval[k] for k in kEig]
    return eigval[ix], eigvec[:, ix]


def randRGB():
    return (random.randint(0, 255) / 255.0,
            random.randint(0, 255) / 255.0,
            random.randint(0, 255) / 255.0)


def plot(matrix, C, centers, k):
    colors = []
    for i in range(k):
        colors.append(randRGB())
    for idx, value in enumerate(C):
        plt.plot(matrix[idx][0], matrix[idx][1], 'o', color=colors[int(C[idx])])
    for i in range(len(centers)):
        plt.plot(centers[i][0], centers[i][1], 'rx')
    plt.show()


# 获得中心位置
# def get_centers(data, C):
#     centers = []
#     for i in range(max(C) + 1):
#         points_list = np.where(C == i)[0].tolist()
#         centers.append(np.average(data[points_list], axis=0))
#     return centers


def calculate_labels(cluster_num):
    W = get_w()
    D = get_d(W)
    L = D - W
    eigval, eigvec = get_eig_vec(L, cluster_num)

    clf = KMeans(n_clusters=cluster_num)
    s = clf.fit(eigvec)
    C = s.labels_

    # centers = get_centers(data, C)
    # plot(data, s.labels_, centers, cluster_num)

    return C


def summarize_result(cluster_num):
    print settings.clusters
    clusters = []
    for i in range(cluster_num):
        clusters.append(settings.Cluster(set()))
    for i in range(len(settings.clusters)):
        c = clusters[labels[i]]
        c.cases |= settings.clusters[i].cases
        c.funcs |= settings.clusters[i].funcs
    return clusters


def print_clusters(clusters):
    print "*****************************************************"
    print "Size of resulting roles: " + str(len(clusters))
    print "*****************************************************"
    for c in clusters:
        print(c)
    print ""


def check_permission_coverage(clusters):
    permissions = set()
    for i in range(len(clusters)):
        permissions |= clusters[i].funcs

    print "*****************************************************"
    print "Size of covered permissions: " + str(len(permissions))
    print "*****************************************************"
    print permissions
    return len(permissions)


def check_overlap(clusters):
    overlap = 0
    for i in range(len(clusters)):
        overlap += len(clusters[i].funcs)
    return overlap


def check_testcase_coverage(clusters):
    cases = set()
    for i in range(len(clusters)):
        cases |= clusters[i].cases

    print "*****************************************************"
    print "Size of covered test cases: " + str(len(cases))
    print "*****************************************************"
    print cases
    return len(cases)


def print_all(covered_permissions, cluster_num, overlap, covered_testcases):
    print "*****************************************************"
    print "#Covered permisions: %d, #roles: %d, #overlaps: %d, #covered test cases: %d" %\
          (covered_permissions, cluster_num, overlap - covered_permissions, covered_testcases)
    print "*****************************************************"


if __name__ == '__main__':
    cluster_num = 14

    test.run_test()

    test.print_links()
    test.print_clusters()

    labels = calculate_labels(cluster_num)
    print labels

    clusters = summarize_result(cluster_num)
    print_clusters(clusters)
    covered_permissions = check_permission_coverage(clusters)
    overlap = check_overlap(clusters)
    covered_testcases = check_testcase_coverage(clusters)
    print_all(covered_permissions, cluster_num, overlap, covered_testcases)


    # graph.generate_force_layout(labels)
