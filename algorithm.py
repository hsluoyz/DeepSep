
import settings
import test


def merge_clusters(c1, c2):
    c = settings.Cluster(c1.cases | c2.cases)
    c.funcs = c1.funcs | c2.funcs
    if c1.level == c2.level:
        c.level = c1.level + 1
        c.children = [c1, c2]
    elif c1.level > c2.level:
        c.level = c1.level
        c.children = list(c1.children)
        c.children.append(c2)
    else:
        c.level = c2.level
        c.children = list(c2.children)
        c.children.append(c1)
    return c


def do_clustering():
    i = 0
    while i < len(settings.clusters):
        j = i + 1
        while j < len(settings.clusters):
            if settings.links[i][j] >= 0:
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
