# coding=gbk

import re
import numpy as np
import pprint

import settings


def method_path_to_string(method, path):
    return path + " | " + method


def init_from_test():
    pattern_uuid = "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    regex_uuid = re.compile(pattern_uuid)

    pattern_id = "[0-9a-f]{32}"
    regex_id = re.compile(pattern_id)

    keywords = [
        # Nova
        "flavors",
        "os-extra_specs",
        "images",
        "os-agents",
        "os-aggregates",
        "os-hosts",
        "os-hypervisors",
        "os-instance_usage_audit_log",
        "os-keypairs",
        "os-quota-sets",
        "os-security-groups",
        "os-simple-tenant-usage",
        "os-volumes",
        "servers",

        "os-fixed-ips",
        "os-security-group-default-rules",

        # Cinder
        "extra_specs",

        # Kubernetes
        "namespaces",
        "pods",
        "jobs",
        "events",
        "persistentvolumeclaims",
        "persistentvolumes",
        "replicationcontrollers",
        "nodes",
        "services",
        "secrets",
        "foo",
        "bindings",
        "clusterrolebindings",
        "extensions",
        "watch",
        "certificates",
        "policy",
        "clusterroles",
        "rbac.authorization.k8s.io",
        "apps",
    ]

    pattern_name = "("
    for keyword in keywords:
        pattern_name += (keyword + "/|")
    pattern_name = pattern_name[:-1]
    pattern_name += ")[^/]+"

    # print "pattern_name = " + pattern_name

    # pattern_name = "(os-simple-tenant-usage/|os-quota-sets/|flavors/|servers/|os-agents/|os-aggregates/|os-fixed-ips/
    # |os-extra_specs/|os-hosts/|os-hypervisors/)[^/]+"
    regex_name = re.compile(pattern_name)

    current_line = ""

    for line in open(settings.filepath + settings.filename):
        # print "AAA" + line + "BBB"
        if line.startswith("#"):
            line = line.strip("\n").strip("#").lstrip('test_')

            # print "\n*****************************************************"
            # print line
            # print "*****************************************************"

            current_line = line

            settings.case_list.append(line)

        else:
            if line == "\n":
                continue

            if settings.filename == "k8s-vectors-new.txt":
                method, path = line.strip("\n").split(',')
            elif line.startswith("2"):
                tmp_list = line.strip("\n").split('\t')
                method = tmp_list[1]
                path = tmp_list[2]
            else:
                continue
            # else:
            #     tmp_list = line.strip("\n").split('|')
            #     method = tmp_list[0].strip(' ')
            #     path = tmp_list[1].strip(' ')

            # print method + " | " + path

            if path.find("128:") != -1:
                path = path[path.find("128:") + 4:]
            path = path.replace("8774", "NOVA")
            path = path.replace("9696", "NEUTRON")
            path = path.replace("9292", "GLANCE")
            path = path.replace("8776", "CINDER")
            path = path.replace("8004", "HEAT")
            path = path.replace("8777", "CEILOMETER")
            path = path.replace("5000", "KEYSTONE")

            path = path.replace("NOVA/v2.1/", "")
            path = path.replace("GLANCE/", "")
            path = path.replace("CINDER/v1/", "")
            path = path.replace("CINDER/v2/", "")

            path = path.replace("/detail", "")

            path = path.replace("/api/v1/", "")

            question_mark = path.find("?")
            if question_mark != -1:
                path = path[:question_mark]

            path = regex_uuid.sub("%UUID%", path)
            path = regex_id.sub("%NAME%", path)
            path = regex_name.sub("\\1%NAME%", path)

            if path.startswith("%NAME%/"):
                path = path[6:]
            path = path.strip("/")

            # print method + " | " + path

            if not settings.test_dict.has_key(current_line):
                settings.test_dict[current_line] = {}
            if not settings.test_dict[current_line].has_key(method_path_to_string(method, path)):
                settings.test_dict[current_line][method_path_to_string(method, path)] = 0
                settings.test_dict[current_line][method_path_to_string(method, path)] += 1

            settings.api_list.append(method_path_to_string(method, path))

    case_list = []
    for case in settings.case_list:
        if settings.test_dict.has_key(case):
            case_list.append(case)
    settings.case_list = case_list


def init_lists():
    # Initialize the test case list.
    settings.case_list = list(set(settings.case_list))
    settings.case_list.sort()
    settings.case_count = len(settings.case_list)

    # Initialize the API list.
    settings.api_list = list(set(settings.api_list))
    settings.api_list.sort()
    settings.api_count = len(settings.api_list)
    settings.category_max_count = settings.api_count / 10


def init_test_matrix():
    m = np.zeros((settings.case_count, settings.api_count), dtype=np.int)
    for i in range(0, settings.case_count):
        for j in range(0, settings.api_count):
            if settings.test_dict[settings.case_list[i]].has_key(settings.api_list[j]):
                # m[i, j] = test_dict[case_list[i]][api_list[j]]
                # We do not calculate the occurrence for now.
                m[i, j] = 1
    return m


def unique_rows(a):
    a = np.ascontiguousarray(a)
    unique_a = np.unique(a.view([('', a.dtype)]*a.shape[1]))
    return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))


def cleanse_test_matrix(m, case_list):
    row_size, col_size = m.shape

    new_m = unique_rows(m)
    new_row_size, _ = new_m.shape
    # print_matrix(new_m)
    new_case_list = [""] * new_row_size

    for i in range(0, row_size):
        for i2 in range(0, new_row_size):
            if tuple(m[i, :]) == tuple(new_m[i2, :]):
                new_case_list[i2] += case_list[i] + ", "

    for i in range(0, len(new_case_list)):
        new_case_list[i] = new_case_list[i].rstrip(', ')

    # print_list(new_case_list)

    return new_m, new_case_list


def row_cover(r1, r2, col_size):
    for i in range(0, col_size):
        if r1[i] < r2[i]:
            return False
    return True


def cleanse_test_matrix2(m, case_list):
    row_size, col_size = m.shape

    new_m = np.empty([0, col_size], dtype=int)
    new_case_list = []
    for i in range(row_size - 1, -1, -1):
        is_covered = False
        new_row_size, _ = new_m.shape
        for i2 in range(0, new_row_size):
            if row_cover(new_m[i2, :], m[i, :], col_size):
                is_covered = True
                new_case_list[i2] = case_list[i] + ", " + new_case_list[i2]
                break
        if not is_covered:
            new_m = np.insert(new_m, 0, values=m[i, :], axis=0)
            new_case_list.insert(0, case_list[i])

    return new_m, new_case_list


def print_labels():
    pprint.pprint(settings.labels)


def print_clusters():
    print "*****************************************************"
    print "Size of clusters: " + str(len(settings.clusters))
    print "*****************************************************"
    for c in settings.clusters:
        print(c)
    print ""


def print_links():
    print "*****************************************************"
    print "Size of links: " + str(len(settings.clusters))
    print "*****************************************************"
    for i in range(len(settings.clusters)):
        print(settings.links[i])
    print ""


def calculate_labels():
    settings.labels = settings.test_dict.keys()
    print_labels()

    for i in range(len(settings.labels)):
        settings.clusters.append(settings.Cluster({i}))
        for func in settings.test_dict[settings.labels[i]]:
            settings.clusters[i].funcs.add(func)

    print_clusters()


def calculate_links():
    size = len(settings.clusters)
    settings.links = [([0] * size) for i in range(size)]
    for i in range(size):
        for j in range(i + 1, size):
            n = min(len(settings.clusters[i].funcs), settings.clusters[j].funcs)
            m = len(settings.clusters[i].funcs & settings.clusters[j].funcs)
            weight = float(m) / n
            # print(keys[i], keys[j], weight)
            settings.links[i][j] = weight


def run_test():
    init_from_test()
    pprint.pprint(settings.case_list)
    pprint.pprint(settings.api_list)
    # pprint.pprint(settings.test_dict)

    calculate_labels()
    calculate_links()
    print_links()


if __name__ == '__main__':
    # m = np.ones([3, 3])
    # n = np.zeros([3, 3])
    # print m
    # print n
    #
    # print np.insert(m, 3, values=n[0, :], axis=0)

    # m = np.array([[2, 1, 3], [0, 0, 0], [1, 1, 1]])
    # print m
    # m = np.dot(m, np.ones([3, 1]))
    # # m = m.transpose()
    # print m

    run_test()
