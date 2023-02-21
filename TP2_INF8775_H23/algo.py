import argparse
import numpy as np
from time import perf_counter
import implementation as algo

SECOND_TO_MS = 1000

if __name__ == '__main__':
    #parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", dest="a", type=str, help="a: algorithm to use {conv, strassen, strassenSeuil}")
    parser.add_argument("-e", dest="e", type=str, help="e: Path to the exemple")
    parser.add_argument("-p", dest="p", type=bool, help="p: print the matrix", default=False, nargs='?')
    parser.add_argument("-t", dest="t", type=bool, help="t: print the time", default=False, nargs='?')
    parser.add_argument("-d", dest="d", type=bool, help="d: print the distance", default=False, nargs='?')
    args = parser.parse_args()

    if args.p is None:
        args.p = True
    if args.t is None:
        args.t = True
    if args.d is None:
        args.d = True

    towns = dict()
    size = 0
    with open(args.e, 'r') as f:
        size = int(f.readline())
        for i in range(size):
            towns[i] = tuple([int(coord) for coord in f.readline().split()])

    start_time = perf_counter()
    if args.a == "glouton":
        result = algo.glouton(size, towns)
    elif args.a == "progdyn":
        result = algo.progdyn(size, towns)
    elif args.a == "approx":
        result = algo.approx(size, towns)
    end_time = perf_counter()

    result.append(result[0])
    if result[1] > result[-2]:
        result.reverse()


    if args.d:
        distance = 0
        for i in range(size):
            distance += algo.euclidean_distance(towns[result[i]], towns[result[i+1]])
        print(str(distance))

    if args.p:
        for townIndex in result:
            print(townIndex)

    if args.t:
        print(str(SECOND_TO_MS*(end_time - start_time)))