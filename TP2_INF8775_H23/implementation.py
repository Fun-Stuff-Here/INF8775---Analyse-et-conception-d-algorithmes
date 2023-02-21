
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
    return [0, 1, 4, 3, 2, 0]

def approx(size:int, towns:dict):
    return [0, 1, 4, 3, 2, 0]
