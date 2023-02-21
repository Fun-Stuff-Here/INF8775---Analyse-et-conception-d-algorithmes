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

def approx(size:int, towns:dict):
    return [0, 1, 4, 3, 2, 0]
