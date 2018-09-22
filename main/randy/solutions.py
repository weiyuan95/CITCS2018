class Node:
    def __init__(self, name):
        self.name = name
        self.edges = []

    def addEdge(self, node):
        self.edges.append(node)


def skill_puzzle(data):
    offensive = data["boss"]["offense"]

    attack_list = []
    offense_list = []
    points_list = []
    nodes = []

    for skill in data["skills"]:
        attack_list.append(skill["name"])
        offense_list.append(skill["offense"])
        points_list.append(skill["points"])

        curr_node = Node(skill["name"])
        nodes.append(curr_node)

        if skill["require"] in attack_list:
            nodes[attack_list.index(skill["require"])].addEdge(curr_node)

    resolved = []
    seen = []

    def dep_resolve(node, resolved, seen):
        resolved.append(node)
        seen.append(node)
        if node not in seen:
            for edge in node.edges:
                if edge not in seen:
                    dep_resolve(edge, resolved, seen)
                else:
                    continue

    for node in nodes:
        dep_resolve(node, resolved, seen)

    for node in resolved:
        print(node.name)
