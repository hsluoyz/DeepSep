# coding=gbk

test_dict = {}

labels = []


class Cluster:
    def __init__(self, cases):
        self.cases = cases
        self.funcs = set()
        self.children = []
        self.level = 0

    def __str__(self):
        return str(self.cases) + ", " + str(self.funcs)

    def get_name(self):
        return ", ".join(map(lambda i: labels[i], self.cases))


clusters = []
links = []

case_list = []
api_list = []
case_count = 0
api_count = 0
category_max_count = 0

full_score = 0

filepath = "J:/OpenStack国家863项目/我的论文/RestSep/实验数据/"
filename = "stack.log.nova"
# filename = "stack.log.keystone"
# filename = "stack.log.glance"
# filename = "stack.log.cinder"
# filename = "k8s-vectors-new.txt"
