
import settings
import test


def merge_clusters(c1, c2):
    c = settings.Cluster(c1.cases | c2.cases)
    c.funcs = c1.funcs | c2.funcs
    return c


def do_clustering():
    i = 0
    while i < len(settings.clusters):
        j = i + 1
        while j < len(settings.clusters):
            if settings.links[i][j] >= 1:
                settings.clusters[i] = merge_clusters(settings.clusters[i], settings.clusters[j])
                del settings.clusters[j]
                test.calculate_links()
            else:
                j += 1
        i += 1


if __name__ == '__main__':
    c1 = settings.Cluster({1})
    c2 = settings.Cluster({2})
    print merge_clusters(c1, c2)
