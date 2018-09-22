from random import randrange

import numpy
import scipy


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
    attack_offense_dict = {}
    attack_point_dict = {}
    nodes = []
    final_attack_list = []

    for skill in data["skills"]:
        attack_list.append(skill["name"])
        offense_list.append(skill["offense"])
        points_list.append(skill["points"])
        attack_point_dict.update({skill["name"]: skill["points"]})
        attack_offense_dict.update({skill["name"]: skill["offense"]})

        curr_node = Node(skill["name"])
        nodes.append(curr_node)

        if skill["require"] in attack_list:
            nodes[attack_list.index(skill["require"])].addEdge(curr_node)

    # print(attack_point_dict)
    # sorted_attack_point_dict = [{k: attack_point_dict[k]} for k in sorted(attack_point_dict, key=attack_point_dict.get)]
    # print(sorted_attack_point_dict)

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

    # for node in resolved:
    #     print(node.name)

    current_offense = 0

    for attack in resolved:
        if current_offense < offensive:
            # print(attack.name)
            current_offense += attack_offense_dict[attack.name]
            # print("current offense: ", current_offense)
            final_attack_list.append(attack.name)
        else:
            break

    return final_attack_list


def machine_learning_1():
    x = [2, 3, 4]
    y = [9]
    answers = []
    unsolved = True

    while unsolved:
        one = randrange(max(x))
        # print(one)
        two = randrange(max(x))
        # print(two)
        three = randrange(max(x))
        # print(three)

        sum = one*x[0] + two*x[1] + three*x[2]
        print(sum)

        if sum == y[0]:
            answers.append(one)
            answers.append(two)
            answers.append(three)
            unsolved = False

    print(answers)

machine_learning_1()