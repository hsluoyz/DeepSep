# coding=gbk

import random
import test
import settings
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans


# 获得相似度矩阵
def get_w():
    size = len(settings.links)
    w = np.zeros((size, size))
    for i in range(size):
        for j in range(i + 1, size):
            w[i][j] = w[j][i] = round(settings.links[i][j], 3)
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


if __name__ == '__main__':
    cluster_num = 5
    test.run_test()
    W = get_w()
    D = get_d(W)
    L = D - W
    eigval, eigvec = get_eig_vec(L, cluster_num)

    clf = KMeans(n_clusters=cluster_num)
    s = clf.fit(eigvec)
    C = s.labels_
    print C

    # centers = get_centers(data, C)
    # plot(data, s.labels_, centers, cluster_num)
