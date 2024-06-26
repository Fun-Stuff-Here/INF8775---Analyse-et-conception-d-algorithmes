import numpy as np

# source : https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset
def powerset(seq):
    """
    Returns all the subsets of this set. This is a generator.
    """
    if len(seq) <= 1:
        yield seq
        yield []
    else:
        for item in powerset(seq[1:]):
            yield [seq[0]]+item
            yield item


def euclidean_distance(town1:tuple, town2:tuple):
    return ((town1[0] - town2[0])**2 + (town1[1] - town2[1])**2)**0.5

def glouton(size:int, towns:dict):

    to_visit = [i for i in range(1, size)]
    result = [0]


    while len(to_visit) > 0:
        min_found, index = float('inf'), float('inf')
        for i in to_visit:
            distance = euclidean_distance(towns[result[-1]], towns[i])
            if distance < min_found:
                min_found, index = distance, i 
        result.append(index)
        to_visit.remove(index)

    return result

def progdyn(size:int, towns:dict):

    town_indexes = list(towns.keys())
    town_indexes.remove(0)
    cols = [set(x) for x in powerset(town_indexes)]
    cols.sort(key=lambda x: len(x))
    cols.pop()
    dyn_table = dict()

    # remplir valeur frontière
    for k in town_indexes:
        dyn_table[(k, frozenset(cols[0]))] = euclidean_distance(towns[0], towns[k]), 0

    # remplir table
    for subset in cols[1:]:
        for k in town_indexes:
            if k in subset:
                dyn_table[(k, frozenset(subset))] = None
            else:
                min_found, min_found_index = float('inf'), float('inf')
                for j in subset:
                    distance = euclidean_distance(towns[k], towns[j]) + dyn_table[(j, frozenset(subset - {j}))][0]
                    if distance < min_found:
                        min_found, min_found_index = distance, j
                dyn_table[(k, frozenset(subset))] = min_found, min_found_index

    # trouver le chemin
    min_path, min_path_index = float('inf'), float('inf')
    town_indexes_set = set(town_indexes)
    for k in town_indexes_set:
        distance = euclidean_distance(towns[0], towns[k]) + dyn_table[(k, frozenset(town_indexes_set - {k}))][0]
        if distance < min_path:
            min_path, min_path_index = distance, k

    def get_path(k:int, town_indexes_set:set):
        if len(town_indexes_set) == 1:
            return [k]
        return [k] + get_path(dyn_table[(k, frozenset(town_indexes_set - {k}))][1], town_indexes_set - {k})

    result = get_path(min_path_index, town_indexes_set)
    result.append(0)
    result.reverse()
    return result

#source : https://www.geeksforgeeks.org/prims-minimum-spanning-tree-mst-greedy-algo-5/
# Prim's Minimum Spanning Tree (MST) algorithm.
import sys

class Graph():
    def __init__(self, vertices, towns:dict):
        self.V = vertices
        self.nodes = {}
        self.towns = towns

    def printMST(self, parent):
        for i in range(1, self.V):
            if parent[i] not in self.nodes:
                self.nodes[parent[i]] = []
            self.nodes[parent[i]].append({"child":i, "weight":euclidean_distance(self.towns[i], self.towns[parent[i]])})
        
        stack = [0]
        result = []
        while len(stack) > 0:
            current = stack.pop()
            result.append(current)
            if current in self.nodes:
                for child in self.nodes[current]:
                    stack.append(child["child"])
        return result

    def minKey(self, key, mstSet):

        # Initialize min value
        min = sys.maxsize

        for v in range(self.V):
            if key[v] < min and mstSet[v] == False:
                min = key[v]
                min_index = v

        return min_index


    def primMST(self):

        key = [sys.maxsize] * self.V
        parent = [None] * self.V
        key[0] = 0
        mstSet = [False] * self.V
        parent[0] = -1
        for cout in range(self.V):
            u = self.minKey(key, mstSet)
            mstSet[u] = True
            for v in range(self.V):
                uv_distance = euclidean_distance(self.towns[u], self.towns[v])
                if uv_distance > 0 and mstSet[v] == False \
                and key[v] > uv_distance:
                    key[v] = uv_distance
                    parent[v] = u

        return self.printMST(parent)

def approx(size:int, towns:dict):
    g = Graph(size, towns)
    return g.primMST()

